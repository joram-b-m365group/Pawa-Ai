"""Base agent interface for multi-agent system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from genius_ai.core.logger import logger
from genius_ai.models.base import BaseModel, GenerationConfig


class AgentRole(str, Enum):
    """Agent roles in the system."""

    ORCHESTRATOR = "orchestrator"
    REASONING = "reasoning"
    PLANNING = "planning"
    CODING = "coding"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    REFLECTION = "reflection"
    TOOL_USER = "tool_user"


@dataclass
class AgentThought:
    """Represents an agent's thought process."""

    content: str
    agent_role: AgentRole
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class AgentAction:
    """Represents an action taken by an agent."""

    action_type: str
    parameters: dict[str, Any]
    result: Any | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class AgentResponse:
    """Response from an agent."""

    content: str
    thoughts: list[AgentThought] = field(default_factory=list)
    actions: list[AgentAction] = field(default_factory=list)
    confidence: float = 1.0
    needs_clarification: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        role: AgentRole,
        model: BaseModel,
        system_prompt: str | None = None,
    ):
        """Initialize agent.

        Args:
            role: Agent's role
            model: Language model to use
            system_prompt: System prompt for the agent
        """
        self.role = role
        self.model = model
        self.system_prompt = system_prompt or self._get_default_prompt()
        self._thought_history: list[AgentThought] = []

    @abstractmethod
    def _get_default_prompt(self) -> str:
        """Get default system prompt for agent."""
        pass

    @abstractmethod
    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Process input and generate response.

        Args:
            input_text: Input to process
            context: Additional context

        Returns:
            Agent response
        """
        pass

    def _add_thought(self, content: str, metadata: dict[str, Any] | None = None) -> AgentThought:
        """Record a thought in the agent's history.

        Args:
            content: Thought content
            metadata: Optional metadata

        Returns:
            Created thought
        """
        thought = AgentThought(
            content=content,
            agent_role=self.role,
            metadata=metadata or {},
        )
        self._thought_history.append(thought)
        logger.debug(f"[{self.role.value}] Thought: {content}")
        return thought

    async def _generate(
        self,
        prompt: str,
        config: GenerationConfig | None = None,
    ) -> str:
        """Generate response from model.

        Args:
            prompt: Input prompt
            config: Generation configuration

        Returns:
            Generated text
        """
        full_prompt = f"{self.system_prompt}\n\n{prompt}"
        response = await self.model.generate(full_prompt, config)
        return response.text

    def get_thoughts(self) -> list[AgentThought]:
        """Get agent's thought history."""
        return self._thought_history.copy()

    def clear_thoughts(self) -> None:
        """Clear thought history."""
        self._thought_history.clear()


class ReasoningAgent(BaseAgent):
    """Agent specialized in logical reasoning and problem decomposition."""

    def __init__(self, model: BaseModel):
        """Initialize reasoning agent."""
        super().__init__(AgentRole.REASONING, model)
        self._decomposition_strategies = {
            "question": self._decompose_question,
            "problem": self._decompose_problem,
            "task": self._decompose_task,
            "analysis": self._decompose_analysis,
        }

    def _get_default_prompt(self) -> str:
        """Get default prompt."""
        return """You are a reasoning agent specialized in logical thinking and problem decomposition.

Your responsibilities:
1. Break down complex problems into smaller, manageable steps
2. Apply logical reasoning to analyze situations
3. Identify assumptions and potential issues
4. Provide clear, structured reasoning chains

Use chain-of-thought reasoning for complex problems. Think step by step."""

    def _classify_input_type(self, text: str) -> str:
        """Classify the type of input for appropriate decomposition strategy.

        Args:
            text: Input text to classify

        Returns:
            Input type (question/problem/task/analysis)
        """
        text_lower = text.lower()

        # Question indicators
        question_words = ["what", "why", "how", "when", "where", "who", "which", "can", "should", "is", "are", "does"]
        if any(text_lower.startswith(word) for word in question_words) or "?" in text:
            return "question"

        # Problem indicators
        problem_words = ["solve", "fix", "debug", "error", "issue", "problem", "wrong", "broken"]
        if any(word in text_lower for word in problem_words):
            return "problem"

        # Task indicators
        task_words = ["create", "build", "implement", "make", "develop", "design", "write", "add"]
        if any(word in text_lower for word in task_words):
            return "task"

        # Default to analysis
        return "analysis"

    def _decompose_question(self, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Decompose a question into sub-questions and required knowledge.

        Args:
            text: Question to decompose
            context: Additional context

        Returns:
            Decomposition structure
        """
        self._add_thought("Decomposing question into sub-questions")

        # Extract key concepts
        # Simple keyword extraction (in production, use NLP)
        words = text.split()
        key_concepts = [w for w in words if len(w) > 4 and w.isalpha()]

        return {
            "type": "question",
            "main_question": text,
            "key_concepts": key_concepts[:5],  # Top 5 concepts
            "sub_questions": [
                f"What do we know about {concept}?" for concept in key_concepts[:3]
            ],
            "requires_knowledge": True,
            "reasoning_steps": [
                "Identify what is being asked",
                "Gather relevant information",
                "Synthesize answer from information",
                "Verify answer completeness"
            ]
        }

    def _decompose_problem(self, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Decompose a problem into diagnosis and solution steps.

        Args:
            text: Problem to decompose
            context: Additional context

        Returns:
            Decomposition structure
        """
        self._add_thought("Decomposing problem into diagnosis and solution steps")

        return {
            "type": "problem",
            "problem_statement": text,
            "diagnosis_steps": [
                "Identify the symptom or error",
                "Determine the root cause",
                "Identify affected components"
            ],
            "solution_steps": [
                "Develop potential solutions",
                "Evaluate solution viability",
                "Implement chosen solution",
                "Verify solution effectiveness"
            ],
            "requires_tools": True,
            "reasoning_steps": [
                "Understand the problem context",
                "Diagnose root cause",
                "Design solution",
                "Validate solution"
            ]
        }

    def _decompose_task(self, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Decompose a task into actionable steps.

        Args:
            text: Task to decompose
            context: Additional context

        Returns:
            Decomposition structure
        """
        self._add_thought("Decomposing task into actionable steps")

        return {
            "type": "task",
            "task_description": text,
            "planning_required": True,
            "action_steps": [
                "Define task requirements and goals",
                "Break down into smaller sub-tasks",
                "Identify dependencies between sub-tasks",
                "Execute sub-tasks in order",
                "Verify completion"
            ],
            "requires_tools": True,
            "reasoning_steps": [
                "Clarify task objectives",
                "Identify necessary resources",
                "Plan execution strategy",
                "Execute and monitor progress"
            ]
        }

    def _decompose_analysis(self, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Decompose an analysis request into analytical steps.

        Args:
            text: Analysis request to decompose
            context: Additional context

        Returns:
            Decomposition structure
        """
        self._add_thought("Decomposing analysis into analytical framework")

        return {
            "type": "analysis",
            "subject": text,
            "analysis_framework": [
                "Define scope of analysis",
                "Gather relevant data",
                "Identify patterns and relationships",
                "Draw conclusions",
                "Provide recommendations"
            ],
            "requires_knowledge": True,
            "reasoning_steps": [
                "Understand analysis objectives",
                "Collect and organize information",
                "Apply analytical methods",
                "Synthesize findings"
            ]
        }

    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Process input with real problem decomposition."""
        self._add_thought(f"Analyzing: {input_text[:100]}...")

        # Step 1: Classify input type
        input_type = self._classify_input_type(input_text)
        self._add_thought(f"Classified as: {input_type}")

        # Step 2: Decompose using appropriate strategy
        decomposition_func = self._decomposition_strategies.get(input_type, self._decompose_analysis)
        decomposition = decomposition_func(input_text, context)
        self._add_thought(f"Decomposed into {len(decomposition.get('reasoning_steps', []))} reasoning steps")

        # Step 3: Build enhanced prompt with decomposition
        prompt = f"""Task: {input_text}

Type: {input_type.capitalize()}

Decomposition Analysis:
{self._format_decomposition(decomposition)}

Now, using this structured decomposition, provide a thorough analysis that:
1. Addresses each reasoning step systematically
2. Identifies key insights and considerations
3. Provides actionable conclusions

Be thorough but concise."""

        if context:
            # Check if we have knowledge from RAG
            if "knowledge" in context:
                prompt += f"\n\nRelevant Knowledge:\n{context['knowledge'][:1000]}..."
                self._add_thought("Incorporated retrieved knowledge into reasoning")

            # Check for conversation history
            if "history" in context:
                prompt += f"\n\nConversation Context: Available"
                self._add_thought("Considering conversation history")

        # Step 4: Generate reasoning response
        response_text = await self._generate(prompt)
        self._add_thought("Completed structured reasoning analysis")

        return AgentResponse(
            content=response_text,
            thoughts=self.get_thoughts(),
            confidence=0.9,
            metadata={
                "input_type": input_type,
                "decomposition": decomposition,
                "reasoning_steps_count": len(decomposition.get("reasoning_steps", [])),
            }
        )

    def _format_decomposition(self, decomposition: dict[str, Any]) -> str:
        """Format decomposition structure for prompt.

        Args:
            decomposition: Decomposition structure

        Returns:
            Formatted string
        """
        lines = []

        if "key_concepts" in decomposition:
            lines.append(f"Key Concepts: {', '.join(decomposition['key_concepts'])}")

        if "sub_questions" in decomposition:
            lines.append("\nSub-Questions:")
            for i, q in enumerate(decomposition['sub_questions'], 1):
                lines.append(f"  {i}. {q}")

        if "diagnosis_steps" in decomposition:
            lines.append("\nDiagnosis Steps:")
            for i, step in enumerate(decomposition['diagnosis_steps'], 1):
                lines.append(f"  {i}. {step}")

        if "solution_steps" in decomposition:
            lines.append("\nSolution Steps:")
            for i, step in enumerate(decomposition['solution_steps'], 1):
                lines.append(f"  {i}. {step}")

        if "action_steps" in decomposition:
            lines.append("\nAction Steps:")
            for i, step in enumerate(decomposition['action_steps'], 1):
                lines.append(f"  {i}. {step}")

        if "analysis_framework" in decomposition:
            lines.append("\nAnalysis Framework:")
            for i, step in enumerate(decomposition['analysis_framework'], 1):
                lines.append(f"  {i}. {step}")

        lines.append(f"\nRequires Knowledge: {decomposition.get('requires_knowledge', False)}")
        lines.append(f"Requires Tools: {decomposition.get('requires_tools', False)}")

        return "\n".join(lines)


class PlanningAgent(BaseAgent):
    """Agent specialized in creating action plans."""

    def __init__(self, model: BaseModel):
        """Initialize planning agent."""
        super().__init__(AgentRole.PLANNING, model)

    def _get_default_prompt(self) -> str:
        """Get default prompt."""
        return """You are a planning agent specialized in creating detailed action plans.

Your responsibilities:
1. Create step-by-step action plans
2. Identify dependencies between steps
3. Estimate effort and complexity
4. Provide contingency planning

Output plans in a clear, structured format."""

    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Process input and create plan."""
        self._add_thought(f"Creating plan for: {input_text}")

        prompt = f"""Task: {input_text}

Create a detailed action plan:
1. List specific steps needed
2. Identify dependencies
3. Note any prerequisites
4. Suggest success criteria

Format as a numbered list with clear steps."""

        if context:
            prompt += f"\n\nContext: {context}"

        response_text = await self._generate(prompt)
        self._add_thought("Plan created")

        return AgentResponse(
            content=response_text,
            thoughts=self.get_thoughts(),
            confidence=0.85,
        )


class ReflectionAgent(BaseAgent):
    """Agent specialized in self-reflection and improvement."""

    def __init__(self, model: BaseModel):
        """Initialize reflection agent."""
        super().__init__(AgentRole.REFLECTION, model)

    def _get_default_prompt(self) -> str:
        """Get default prompt."""
        return """You are a reflection agent specialized in critiquing and improving responses.

Your responsibilities:
1. Analyze responses for quality and accuracy
2. Identify potential improvements
3. Check for logical consistency
4. Suggest refinements

Be constructively critical and thorough."""

    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Reflect on and improve input."""
        self._add_thought(f"Reflecting on: {input_text[:100]}...")

        prompt = f"""Analyze this response and provide constructive feedback:

{input_text}

Evaluate:
1. Clarity and coherence
2. Accuracy and completeness
3. Potential improvements
4. Any issues or concerns

Provide specific, actionable feedback."""

        if context:
            prompt += f"\n\nOriginal task: {context.get('original_task', 'N/A')}"

        response_text = await self._generate(prompt)
        self._add_thought("Reflection complete")

        return AgentResponse(
            content=response_text,
            thoughts=self.get_thoughts(),
            confidence=0.8,
        )
