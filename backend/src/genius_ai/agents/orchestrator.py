"""Orchestrator agent that coordinates other agents."""

from typing import Any, AsyncIterator

from genius_ai.agents.base import (
    AgentResponse,
    BaseAgent,
    AgentRole,
    PlanningAgent,
    ReasoningAgent,
    ReflectionAgent,
    AgentThought,
)
from genius_ai.core.logger import logger
from genius_ai.models.base import BaseModel
from genius_ai.memory.learning import learning_system


class OrchestratorAgent(BaseAgent):
    """Coordinates multiple specialized agents to solve complex tasks."""

    def __init__(
        self,
        model: BaseModel,
        enable_reflection: bool = True,
        enable_tools: bool = True,
        rag_retriever: Any = None,
    ):
        """Initialize orchestrator.

        Args:
            model: Language model
            enable_reflection: Whether to use reflection agent
            enable_tools: Whether to use tool execution
            rag_retriever: RAG retriever instance for knowledge base
        """
        super().__init__(AgentRole.ORCHESTRATOR, model)
        self.enable_reflection = enable_reflection
        self.enable_tools = enable_tools
        self.rag_retriever = rag_retriever

        # Initialize sub-agents
        self.reasoning_agent = ReasoningAgent(model)
        self.planning_agent = PlanningAgent(model)
        self.reflection_agent = ReflectionAgent(model) if enable_reflection else None

        # Import tool user agent dynamically to avoid circular imports
        if enable_tools:
            from genius_ai.agents.tool_user import ToolUserAgent
            self.tool_user_agent = ToolUserAgent(model)
        else:
            self.tool_user_agent = None

        self._iteration_count = 0
        self._max_iterations = 10
        self._thought_stream_callback = None

    def _get_default_prompt(self) -> str:
        """Get default prompt."""
        return """You are an orchestrator agent that coordinates multiple specialized agents.

Your responsibilities:
1. Analyze tasks and determine which agents to use
2. Coordinate information flow between agents
3. Synthesize responses from multiple agents
4. Ensure high-quality final output

You have access to:
- Reasoning Agent: Logical analysis and problem decomposition
- Planning Agent: Action planning and task sequencing
- Reflection Agent: Response critique and improvement

Coordinate these agents effectively to produce the best possible response."""

    def set_thought_stream_callback(self, callback):
        """Set callback for streaming thoughts in real-time.

        Args:
            callback: Async function to call with each thought
        """
        self._thought_stream_callback = callback

    async def _emit_thought(self, thought: AgentThought):
        """Emit a thought to the stream callback if set.

        Args:
            thought: Thought to emit
        """
        if self._thought_stream_callback:
            await self._thought_stream_callback(thought)

    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Process input using intelligent multi-agent coordination with RAG and tools.

        Args:
            input_text: User input
            context: Additional context

        Returns:
            Orchestrated response with full reasoning chain
        """
        self._iteration_count = 0
        thought = self._add_thought(f"Processing request: {input_text[:100]}...")
        await self._emit_thought(thought)

        # Enhanced context with RAG retrieval
        enhanced_context = context or {}

        # Step 0: RAG Retrieval (if available and not already in context)
        if self.rag_retriever and "knowledge" not in enhanced_context:
            thought = self._add_thought("Retrieving relevant knowledge from database")
            await self._emit_thought(thought)

            try:
                retrieved_context = await self.rag_retriever.retrieve_context(
                    query=input_text,
                    top_k=5,
                )
                if retrieved_context:
                    enhanced_context["knowledge"] = retrieved_context
                    thought = self._add_thought(f"Retrieved {len(retrieved_context.split('---'))} relevant documents")
                    await self._emit_thought(thought)
                else:
                    thought = self._add_thought("No relevant documents found in knowledge base")
                    await self._emit_thought(thought)
            except Exception as e:
                logger.error(f"RAG retrieval error: {e}")
                thought = self._add_thought(f"RAG retrieval failed: {str(e)}")
                await self._emit_thought(thought)

        # Step 1: Reasoning - Analyze the task with RAG context
        thought = self._add_thought("Engaging reasoning agent for structured analysis")
        await self._emit_thought(thought)

        reasoning_response = await self.reasoning_agent.process(input_text, enhanced_context)
        logger.info("Reasoning analysis complete")

        # Emit reasoning thoughts
        for rt in reasoning_response.thoughts:
            await self._emit_thought(rt)

        thought = self._add_thought(
            f"Reasoning complete: classified as {reasoning_response.metadata.get('input_type', 'unknown')}"
        )
        await self._emit_thought(thought)

        # Step 2: Check if tools are needed
        tool_response = None
        decomposition = reasoning_response.metadata.get("decomposition", {})
        needs_tools = decomposition.get("requires_tools", False)

        if self.enable_tools and self.tool_user_agent and needs_tools:
            thought = self._add_thought("Task requires tools - engaging tool user agent")
            await self._emit_thought(thought)

            tool_response = await self.tool_user_agent.process(input_text, enhanced_context)

            # Emit tool thoughts
            for tt in tool_response.thoughts:
                await self._emit_thought(tt)

            if tool_response.actions:
                thought = self._add_thought(f"Executed {len(tool_response.actions)} tool(s)")
                await self._emit_thought(thought)

                # Add tool results to context
                enhanced_context["tool_results"] = {
                    "count": len(tool_response.actions),
                    "tools_used": tool_response.metadata.get("tools_used", []),
                    "summary": tool_response.content,
                }

        # Step 3: Planning - Create action plan
        thought = self._add_thought("Engaging planning agent for action plan")
        await self._emit_thought(thought)

        planning_context = {
            "reasoning": reasoning_response.content,
            "decomposition": decomposition,
            **enhanced_context,
        }

        planning_response = await self.planning_agent.process(input_text, planning_context)
        logger.info("Action plan created")

        # Emit planning thoughts
        for pt in planning_response.thoughts:
            await self._emit_thought(pt)

        # Step 4: Generate initial response synthesizing all information
        thought = self._add_thought("Synthesizing final response from all agent outputs")
        await self._emit_thought(thought)

        initial_response = await self._generate_response(
            input_text,
            reasoning_response.content,
            planning_response.content,
            tool_results=tool_response.content if tool_response else None,
            knowledge=enhanced_context.get("knowledge"),
        )

        # Step 5: Reflection (if enabled)
        final_response = initial_response
        if self.enable_reflection and self.reflection_agent:
            thought = self._add_thought("Engaging reflection agent for quality improvement")
            await self._emit_thought(thought)

            reflection_context = {
                "original_task": input_text,
                "reasoning": reasoning_response.content,
                "plan": planning_response.content,
                "tool_results": tool_response.content if tool_response else None,
            }
            reflection_response = await self.reflection_agent.process(
                initial_response,
                reflection_context,
            )
            logger.info("Reflection complete")

            # Emit reflection thoughts
            for reft in reflection_response.thoughts:
                await self._emit_thought(reft)

            # Check if improvements are suggested
            if "improve" in reflection_response.content.lower():
                thought = self._add_thought("Applying improvements from reflection")
                await self._emit_thought(thought)

                final_response = await self._apply_improvements(
                    initial_response,
                    reflection_response.content,
                )

        thought = self._add_thought("Multi-agent processing complete")
        await self._emit_thought(thought)

        # Collect all thoughts from sub-agents
        all_thoughts = self.get_thoughts() + reasoning_response.thoughts + planning_response.thoughts

        if tool_response:
            all_thoughts += tool_response.thoughts

        if self.enable_reflection and self.reflection_agent:
            all_thoughts += reflection_response.thoughts

        # Collect all actions
        all_actions = []
        if tool_response:
            all_actions.extend(tool_response.actions)

        # Learning: Record the strategy used
        problem_type = reasoning_response.metadata.get("input_type", "unknown")
        approach_summary = f"Multi-agent: reasoning + planning"
        if tool_response:
            approach_summary += f" + tools({', '.join(tool_response.metadata.get('tools_used', []))})"
        if "knowledge" in enhanced_context:
            approach_summary += " + RAG"
        if self.enable_reflection:
            approach_summary += " + reflection"

        # Record as successful (we'll update based on feedback later)
        learning_system.record_strategy(
            problem_type=problem_type,
            approach=approach_summary,
            success=True,  # Assume success initially
            confidence=0.95,
            metadata={
                "tools_used": tool_response.metadata.get("tools_used", []) if tool_response else [],
                "rag_used": "knowledge" in enhanced_context,
                "reflection_used": self.enable_reflection,
                "timestamp": thought.timestamp.isoformat(),
            }
        )

        # Get learning insights for this problem type
        suggestions = learning_system.suggest_improvements(problem_type)
        if suggestions:
            logger.info(f"Learning suggestions for {problem_type}: {suggestions}")

        return AgentResponse(
            content=final_response,
            thoughts=all_thoughts,
            actions=all_actions,
            confidence=0.95,
            metadata={
                "reasoning": reasoning_response.content,
                "reasoning_metadata": reasoning_response.metadata,
                "plan": planning_response.content,
                "tools_used": tool_response.metadata.get("tools_used", []) if tool_response else [],
                "rag_used": "knowledge" in enhanced_context,
                "iterations": self._iteration_count,
                "problem_type": problem_type,
                "approach": approach_summary,
                "learning_suggestions": suggestions,
            },
        )

    async def _generate_response(
        self,
        task: str,
        reasoning: str,
        plan: str,
        tool_results: str | None = None,
        knowledge: str | None = None,
    ) -> str:
        """Generate response based on reasoning, planning, tools, and knowledge.

        Args:
            task: Original task
            reasoning: Reasoning analysis
            plan: Action plan
            tool_results: Results from tool execution (if any)
            knowledge: Retrieved knowledge from RAG (if any)

        Returns:
            Generated response
        """
        prompt = f"""Task: {task}

Reasoning Analysis:
{reasoning}

Action Plan:
{plan}
"""

        if knowledge:
            prompt += f"""
Retrieved Knowledge:
{knowledge[:2000]}...  # Truncate for prompt size
"""

        if tool_results:
            prompt += f"""
Tool Execution Results:
{tool_results}
"""

        prompt += """
Based on the above analysis, plan, and available information, provide a comprehensive response to the task.
Be clear, thorough, and actionable. Integrate all sources of information coherently."""

        response = await self._generate(prompt)
        return response

    async def _apply_improvements(
        self,
        original_response: str,
        feedback: str,
    ) -> str:
        """Apply improvements based on reflection feedback.

        Args:
            original_response: Original response
            feedback: Reflection feedback

        Returns:
            Improved response
        """
        prompt = f"""Original Response:
{original_response}

Feedback:
{feedback}

Improve the original response based on the feedback. Keep what works well and address the concerns raised."""

        improved = await self._generate(prompt)
        return improved

    def reset(self) -> None:
        """Reset orchestrator state."""
        self._iteration_count = 0
        self.clear_thoughts()
        self.reasoning_agent.clear_thoughts()
        self.planning_agent.clear_thoughts()
        if self.reflection_agent:
            self.reflection_agent.clear_thoughts()
