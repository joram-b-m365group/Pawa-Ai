"""
Smart Model Router - Intelligently selects the best AI model based on task
"""

from typing import Dict, Any, Optional
from enum import Enum
import re


class TaskType(Enum):
    """Different types of tasks"""
    CODING = "coding"
    DEBUGGING = "debugging"
    EXPLANATION = "explanation"
    CREATIVE_WRITING = "creative_writing"
    DATA_ANALYSIS = "data_analysis"
    QUICK_QUESTION = "quick_question"
    COMPLEX_REASONING = "complex_reasoning"
    IMAGE_ANALYSIS = "image_analysis"
    DOCUMENT_ANALYSIS = "document_analysis"


class ModelProvider(Enum):
    """Available model providers"""
    GROQ_LLAMA = "groq_llama"
    CLAUDE = "claude"
    GEMINI = "gemini"
    LOCAL = "local"


class SmartModelRouter:
    """
    Intelligently routes requests to the best AI model based on:
    - Task type
    - Urgency (speed vs quality)
    - Context size
    - User preferences
    """

    def __init__(self):
        # Model capabilities matrix
        self.model_specs = {
            # Groq Models (Free, Fast)
            "llama-3.3-70b-versatile": {
                "provider": ModelProvider.GROQ_LLAMA,
                "strengths": ["coding", "general", "fast"],
                "context_window": 8192,
                "speed": "fast",
                "quality": "high",
                "cost": "free"
            },
            "llama-3.2-90b-vision-preview": {
                "provider": ModelProvider.GROQ_LLAMA,
                "strengths": ["vision", "image_analysis"],
                "context_window": 8192,
                "speed": "medium",
                "quality": "high",
                "cost": "free"
            },
            "llama-3.1-8b-instant": {
                "provider": ModelProvider.GROQ_LLAMA,
                "strengths": ["quick_answers", "fast_responses"],
                "context_window": 8192,
                "speed": "very_fast",
                "quality": "medium",
                "cost": "free"
            },

            # Claude Models (Premium, Best Quality)
            "claude-3-5-sonnet-20241022": {
                "provider": ModelProvider.CLAUDE,
                "strengths": ["coding", "reasoning", "analysis", "best_quality"],
                "context_window": 200000,
                "speed": "medium",
                "quality": "best",
                "cost": "paid"
            },
            "claude-3-opus-20240229": {
                "provider": ModelProvider.CLAUDE,
                "strengths": ["complex_reasoning", "creative_writing", "detailed_analysis"],
                "context_window": 200000,
                "speed": "slow",
                "quality": "best",
                "cost": "paid"
            },
            "claude-3-haiku-20240307": {
                "provider": ModelProvider.CLAUDE,
                "strengths": ["speed", "quick_answers"],
                "context_window": 200000,
                "speed": "very_fast",
                "quality": "high",
                "cost": "paid"
            },

            # Google Gemini Models (FREE, Massive Context!)
            "gemini-1.5-pro-latest": {
                "provider": ModelProvider.GEMINI,
                "strengths": ["long_documents", "large_codebases", "massive_context"],
                "context_window": 2000000,  # 2 MILLION tokens!
                "speed": "medium",
                "quality": "best",
                "cost": "free"
            },
            "gemini-1.5-flash-latest": {
                "provider": ModelProvider.GEMINI,
                "strengths": ["speed", "large_context"],
                "context_window": 1000000,  # 1 MILLION tokens
                "speed": "fast",
                "quality": "high",
                "cost": "free"
            }
        }

    def detect_task_type(self, message: str, has_image: bool = False, has_document: bool = False) -> TaskType:
        """Detect what type of task the user is requesting"""
        message_lower = message.lower()

        # Image analysis
        if has_image:
            return TaskType.IMAGE_ANALYSIS

        # Document analysis
        if has_document or any(word in message_lower for word in ["pdf", "document", "paper", "analyze document"]):
            return TaskType.DOCUMENT_ANALYSIS

        # Coding
        if any(word in message_lower for word in [
            "code", "function", "class", "api", "bug", "error", "implement",
            "create app", "build", "develop", "write code", "program"
        ]):
            if any(word in message_lower for word in ["bug", "error", "debug", "fix", "not working"]):
                return TaskType.DEBUGGING
            return TaskType.CODING

        # Complex reasoning
        if any(word in message_lower for word in [
            "explain complex", "architecture", "design pattern", "why",
            "how does", "analyze", "compare", "evaluate"
        ]):
            return TaskType.COMPLEX_REASONING

        # Creative writing
        if any(word in message_lower for word in [
            "write", "story", "essay", "article", "content",
            "blog", "creative", "generate text"
        ]):
            return TaskType.CREATIVE_WRITING

        # Data analysis
        if any(word in message_lower for word in [
            "data", "analyze", "statistics", "metrics",
            "calculate", "numbers", "dataset"
        ]):
            return TaskType.DATA_ANALYSIS

        # Quick question (short messages)
        if len(message.split()) < 10:
            return TaskType.QUICK_QUESTION

        # Default to explanation
        return TaskType.EXPLANATION

    def select_best_model(
        self,
        task_type: TaskType,
        urgency: str = "balanced",  # fast, balanced, quality
        use_paid: bool = False,  # Whether to use paid models (Claude)
        context_size: int = 0
    ) -> str:
        """
        Select the best model based on task and preferences

        Args:
            task_type: The type of task
            urgency: Speed preference (fast/balanced/quality)
            use_paid: Whether to use paid models like Claude
            context_size: Size of context in tokens

        Returns:
            Model ID string
        """

        # Task-specific model selection
        if task_type == TaskType.IMAGE_ANALYSIS:
            return "llama-3.2-90b-vision-preview"

        # If context is VERY LARGE (>8K tokens), use Gemini (FREE!)
        if context_size > 8000:
            return "gemini-1.5-pro-latest"  # 2M tokens, FREE!

        # If Claude is available and user wants best quality
        if use_paid:
            if task_type in [TaskType.CODING, TaskType.DEBUGGING]:
                return "claude-3-5-sonnet-20241022"  # Best for coding

            if task_type == TaskType.COMPLEX_REASONING:
                return "claude-3-opus-20240229"  # Most capable

            if urgency == "fast":
                return "claude-3-haiku-20240307"  # Fastest Claude

            return "claude-3-5-sonnet-20241022"  # Default Claude

        # Free models (Groq/Llama)
        if urgency == "fast" or task_type == TaskType.QUICK_QUESTION:
            return "llama-3.1-8b-instant"  # Fastest

        if task_type in [TaskType.CODING, TaskType.DEBUGGING, TaskType.COMPLEX_REASONING]:
            return "llama-3.3-70b-versatile"  # Best free model

        # Default
        return "llama-3.3-70b-versatile"

    def route_request(
        self,
        message: str,
        has_image: bool = False,
        has_document: bool = False,
        urgency: str = "balanced",
        use_paid: bool = False,
        context_size: int = 0
    ) -> Dict[str, Any]:
        """
        Main routing function - analyzes request and returns best model + metadata

        Returns:
            {
                "model": "model-id",
                "task_type": "coding",
                "provider": "groq_llama",
                "reasoning": "Selected because..."
            }
        """

        # Detect task type
        task_type = self.detect_task_type(message, has_image, has_document)

        # Select best model
        model_id = self.select_best_model(
            task_type=task_type,
            urgency=urgency,
            use_paid=use_paid,
            context_size=context_size
        )

        model_info = self.model_specs.get(model_id, {})

        return {
            "model": model_id,
            "task_type": task_type.value,
            "provider": model_info.get("provider", ModelProvider.GROQ_LLAMA).value,
            "reasoning": self._get_selection_reasoning(task_type, model_id, urgency),
            "estimated_speed": model_info.get("speed", "medium"),
            "estimated_quality": model_info.get("quality", "high")
        }

    def _get_selection_reasoning(self, task_type: TaskType, model_id: str, urgency: str) -> str:
        """Generate human-readable reasoning for model selection"""
        reasons = []

        if "claude" in model_id:
            reasons.append("Using Claude for highest quality")
        else:
            reasons.append("Using free Llama model")

        if task_type == TaskType.CODING:
            reasons.append("optimized for coding tasks")
        elif task_type == TaskType.IMAGE_ANALYSIS:
            reasons.append("with vision capabilities")
        elif task_type == TaskType.QUICK_QUESTION:
            reasons.append("for fast response")

        if urgency == "fast":
            reasons.append("prioritizing speed")
        elif urgency == "quality":
            reasons.append("prioritizing quality")

        return " - ".join(reasons)


# Global router instance
smart_router = SmartModelRouter()
