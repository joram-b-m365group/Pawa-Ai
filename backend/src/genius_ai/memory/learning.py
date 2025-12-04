"""Learning mechanisms for continuous improvement."""

import json
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from genius_ai.core.config import settings
from genius_ai.core.logger import logger


@dataclass
class Strategy:
    """Represents a learned strategy."""

    strategy_id: str
    problem_type: str
    approach: str
    success_count: int
    failure_count: int
    avg_confidence: float
    last_used: str
    metadata: dict[str, Any]

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0


@dataclass
class Feedback:
    """User feedback on a response."""

    conversation_id: str
    message_id: str
    rating: int  # 1-5 scale
    is_positive: bool
    comment: str | None
    timestamp: str
    metadata: dict[str, Any]


class LearningSystem:
    """System for learning from interactions and improving over time."""

    def __init__(self, storage_path: Path | None = None):
        """Initialize learning system.

        Args:
            storage_path: Path to store learning data
        """
        self.storage_path = storage_path or Path(settings.data_dir) / "learning"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.strategies_file = self.storage_path / "strategies.json"
        self.feedback_file = self.storage_path / "feedback.json"

        # In-memory caches
        self._strategies: dict[str, Strategy] = {}
        self._feedback: list[Feedback] = []
        self._problem_type_stats: dict[str, dict] = defaultdict(lambda: {
            "total_attempts": 0,
            "successful": 0,
            "failed": 0,
        })

        # Load existing data
        self._load_data()

    def _load_data(self):
        """Load learning data from disk."""
        # Load strategies
        if self.strategies_file.exists():
            try:
                with open(self.strategies_file, 'r') as f:
                    data = json.load(f)
                    self._strategies = {
                        sid: Strategy(**sdata) for sid, sdata in data.items()
                    }
                logger.info(f"Loaded {len(self._strategies)} strategies")
            except Exception as e:
                logger.error(f"Error loading strategies: {e}")

        # Load feedback
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    self._feedback = [Feedback(**fdata) for fdata in data]
                logger.info(f"Loaded {len(self._feedback)} feedback entries")
            except Exception as e:
                logger.error(f"Error loading feedback: {e}")

        # Rebuild stats
        self._rebuild_stats()

    def _save_strategies(self):
        """Save strategies to disk."""
        try:
            with open(self.strategies_file, 'w') as f:
                data = {sid: asdict(strategy) for sid, strategy in self._strategies.items()}
                json.dump(data, f, indent=2)
            logger.debug("Strategies saved to disk")
        except Exception as e:
            logger.error(f"Error saving strategies: {e}")

    def _save_feedback(self):
        """Save feedback to disk."""
        try:
            with open(self.feedback_file, 'w') as f:
                data = [asdict(fb) for fb in self._feedback]
                json.dump(data, f, indent=2)
            logger.debug("Feedback saved to disk")
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")

    def _rebuild_stats(self):
        """Rebuild problem type statistics from strategies."""
        self._problem_type_stats.clear()

        for strategy in self._strategies.values():
            pt = strategy.problem_type
            stats = self._problem_type_stats[pt]
            stats["total_attempts"] += strategy.success_count + strategy.failure_count
            stats["successful"] += strategy.success_count
            stats["failed"] += strategy.failure_count

    def record_strategy(
        self,
        problem_type: str,
        approach: str,
        success: bool,
        confidence: float,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Record a strategy use and outcome.

        Args:
            problem_type: Type of problem (question/task/problem/analysis)
            approach: Approach taken
            success: Whether the strategy was successful
            confidence: Confidence score
            metadata: Additional metadata

        Returns:
            Strategy ID
        """
        # Generate strategy ID
        strategy_id = f"{problem_type}_{hash(approach) % 10000}"

        # Get or create strategy
        if strategy_id in self._strategies:
            strategy = self._strategies[strategy_id]
            if success:
                strategy.success_count += 1
            else:
                strategy.failure_count += 1

            # Update average confidence
            total = strategy.success_count + strategy.failure_count
            strategy.avg_confidence = (
                (strategy.avg_confidence * (total - 1) + confidence) / total
            )
            strategy.last_used = datetime.now().isoformat()
            strategy.metadata.update(metadata or {})
        else:
            # Create new strategy
            strategy = Strategy(
                strategy_id=strategy_id,
                problem_type=problem_type,
                approach=approach,
                success_count=1 if success else 0,
                failure_count=0 if success else 1,
                avg_confidence=confidence,
                last_used=datetime.now().isoformat(),
                metadata=metadata or {},
            )
            self._strategies[strategy_id] = strategy

        # Update stats
        stats = self._problem_type_stats[problem_type]
        stats["total_attempts"] += 1
        if success:
            stats["successful"] += 1
        else:
            stats["failed"] += 1

        # Save to disk
        self._save_strategies()

        logger.info(f"Recorded strategy {strategy_id}: success={success}, confidence={confidence:.2f}")

        return strategy_id

    def get_best_strategies(
        self,
        problem_type: str,
        top_k: int = 3,
        min_success_rate: float = 0.5,
    ) -> list[Strategy]:
        """Get the best strategies for a problem type.

        Args:
            problem_type: Type of problem
            top_k: Number of top strategies to return
            min_success_rate: Minimum success rate threshold

        Returns:
            List of top strategies
        """
        # Filter strategies by problem type
        relevant = [
            s for s in self._strategies.values()
            if s.problem_type == problem_type and s.success_rate >= min_success_rate
        ]

        # Sort by success rate and confidence
        relevant.sort(
            key=lambda s: (s.success_rate, s.avg_confidence),
            reverse=True,
        )

        return relevant[:top_k]

    def record_feedback(
        self,
        conversation_id: str,
        message_id: str,
        rating: int,
        comment: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Record user feedback on a response.

        Args:
            conversation_id: Conversation ID
            message_id: Message ID
            rating: Rating (1-5)
            comment: Optional comment
            metadata: Additional metadata
        """
        feedback = Feedback(
            conversation_id=conversation_id,
            message_id=message_id,
            rating=rating,
            is_positive=rating >= 4,
            comment=comment,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {},
        )

        self._feedback.append(feedback)
        self._save_feedback()

        logger.info(f"Recorded feedback: rating={rating}, positive={feedback.is_positive}")

    def get_problem_type_stats(self, problem_type: str | None = None) -> dict[str, Any]:
        """Get statistics for a problem type or all types.

        Args:
            problem_type: Specific problem type or None for all

        Returns:
            Statistics dictionary
        """
        if problem_type:
            stats = self._problem_type_stats.get(problem_type, {
                "total_attempts": 0,
                "successful": 0,
                "failed": 0,
            })
            stats["success_rate"] = (
                stats["successful"] / stats["total_attempts"]
                if stats["total_attempts"] > 0 else 0.0
            )
            return stats

        # Return all stats
        all_stats = {}
        for pt, stats in self._problem_type_stats.items():
            stats = dict(stats)
            stats["success_rate"] = (
                stats["successful"] / stats["total_attempts"]
                if stats["total_attempts"] > 0 else 0.0
            )
            all_stats[pt] = stats

        return all_stats

    def get_insights(self) -> dict[str, Any]:
        """Get insights from learning data.

        Returns:
            Dictionary of insights
        """
        total_strategies = len(self._strategies)
        total_feedback = len(self._feedback)
        positive_feedback = sum(1 for f in self._feedback if f.is_positive)

        # Calculate overall success rates
        problem_type_success = {}
        for pt, stats in self._problem_type_stats.items():
            if stats["total_attempts"] > 0:
                problem_type_success[pt] = stats["successful"] / stats["total_attempts"]

        # Best performing problem type
        best_problem_type = max(
            problem_type_success.items(),
            key=lambda x: x[1],
            default=(None, 0)
        )

        # Most common problem type
        most_common = max(
            self._problem_type_stats.items(),
            key=lambda x: x[1]["total_attempts"],
            default=(None, {"total_attempts": 0})
        )

        return {
            "total_strategies": total_strategies,
            "total_feedback": total_feedback,
            "positive_feedback_count": positive_feedback,
            "positive_feedback_rate": positive_feedback / total_feedback if total_feedback > 0 else 0.0,
            "problem_type_success_rates": problem_type_success,
            "best_performing_type": best_problem_type[0],
            "best_performing_rate": best_problem_type[1],
            "most_common_type": most_common[0],
            "most_common_count": most_common[1]["total_attempts"],
        }

    def suggest_improvements(self, problem_type: str) -> list[str]:
        """Suggest improvements based on learning data.

        Args:
            problem_type: Problem type to analyze

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        stats = self._problem_type_stats.get(problem_type)
        if not stats or stats["total_attempts"] == 0:
            suggestions.append(f"No data yet for {problem_type} problems")
            return suggestions

        success_rate = stats["successful"] / stats["total_attempts"]

        if success_rate < 0.5:
            suggestions.append(f"Low success rate ({success_rate:.1%}) for {problem_type} - consider alternative approaches")

            # Get best strategies
            best = self.get_best_strategies(problem_type, top_k=1)
            if best:
                suggestions.append(f"Try approach: {best[0].approach}")

        elif success_rate >= 0.8:
            suggestions.append(f"High success rate ({success_rate:.1%}) - current strategies are working well")

        # Check for strategies that haven't been tried much
        low_usage_strategies = [
            s for s in self._strategies.values()
            if s.problem_type == problem_type
            and (s.success_count + s.failure_count) < 3
        ]

        if low_usage_strategies:
            suggestions.append(f"Consider testing {len(low_usage_strategies)} underutilized strategies")

        return suggestions


# Global learning system instance
learning_system = LearningSystem()
