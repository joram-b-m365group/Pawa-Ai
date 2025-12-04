"""Agent specialized in tool usage and execution."""

import json
import re
from typing import Any

from genius_ai.agents.base import (
    AgentResponse,
    BaseAgent,
    AgentRole,
    AgentAction,
)
from genius_ai.core.logger import logger
from genius_ai.models.base import BaseModel
from genius_ai.tools.base import tool_registry, ToolResult


class ToolUserAgent(BaseAgent):
    """Agent that can use tools to accomplish tasks."""

    def __init__(self, model: BaseModel):
        """Initialize tool user agent."""
        super().__init__(AgentRole.TOOL_USER, model)
        self.tool_registry = tool_registry
        self._max_tool_iterations = 5

    def _get_default_prompt(self) -> str:
        """Get default prompt."""
        return """You are a tool user agent specialized in using tools to accomplish tasks.

Your responsibilities:
1. Analyze tasks to determine if tools are needed
2. Select appropriate tools for the task
3. Execute tools with correct parameters
4. Interpret tool results
5. Combine tool results into a coherent response

Available tools and when to use them:
- calculator: For mathematical calculations and expressions
- search: For finding information (use RAG for knowledge base)
- execute_code: For running Python code, data analysis, or testing
- web_scrape: For extracting content from URLs

Always think step-by-step about which tools to use and why."""

    def _analyze_tool_needs(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Analyze task to determine which tools are needed.

        Args:
            task: Task description
            context: Additional context

        Returns:
            Analysis of tool needs
        """
        task_lower = task.lower()
        needed_tools = []

        # Check for calculation needs
        calc_indicators = ["calculate", "compute", "solve", "math", "+", "-", "*", "/", "sqrt", "sin", "cos"]
        if any(indicator in task_lower for indicator in calc_indicators):
            # Check if there's a mathematical expression
            if re.search(r'\d+\s*[+\-*/]\s*\d+', task) or any(word in task_lower for word in ["sqrt", "sin", "cos", "pow"]):
                needed_tools.append({
                    "tool": "calculator",
                    "reason": "Task involves mathematical calculations",
                })

        # Check for code execution needs
        code_indicators = ["python", "code", "script", "execute", "run", "program", "function"]
        if any(indicator in task_lower for indicator in code_indicators):
            if "```python" in task or "def " in task or "import " in task:
                needed_tools.append({
                    "tool": "execute_code",
                    "reason": "Task involves code execution",
                })

        # Check for search needs
        search_indicators = ["search", "find information", "look up", "what is", "who is", "tell me about"]
        if any(indicator in task_lower for indicator in search_indicators):
            # Check if RAG knowledge might be sufficient
            if context and "knowledge" in context:
                needed_tools.append({
                    "tool": "rag_retriever",
                    "reason": "Information available in knowledge base",
                })
            else:
                needed_tools.append({
                    "tool": "search",
                    "reason": "Task requires external information",
                })

        # Check for web scraping needs
        web_indicators = ["http://", "https://", "website", "webpage", "url"]
        if any(indicator in task_lower for indicator in web_indicators):
            needed_tools.append({
                "tool": "web_scrape",
                "reason": "Task involves web content",
            })

        return {
            "needs_tools": len(needed_tools) > 0,
            "tools": needed_tools,
            "analysis": f"Identified {len(needed_tools)} potential tools for this task",
        }

    def _extract_tool_parameters(self, task: str, tool_name: str) -> dict[str, Any]:
        """Extract parameters for a specific tool from the task.

        Args:
            task: Task description
            tool_name: Name of the tool

        Returns:
            Extracted parameters
        """
        if tool_name == "calculator":
            # Extract mathematical expression
            # Look for expression patterns
            match = re.search(r'(?:calculate|compute|solve)\s+(.+?)(?:\.|$)', task, re.IGNORECASE)
            if match:
                expression = match.group(1).strip()
                return {"expression": expression}

            # Try to find any mathematical expression
            match = re.search(r'(\d+\s*[+\-*/^]\s*\d+(?:\s*[+\-*/^]\s*\d+)*)', task)
            if match:
                return {"expression": match.group(1).strip()}

            # Look for function calls
            match = re.search(r'(sqrt|sin|cos|tan|log|exp)\s*\(\s*\d+\s*\)', task)
            if match:
                return {"expression": match.group(0).strip()}

            return {"expression": ""}

        elif tool_name == "execute_code":
            # Extract Python code from code blocks
            match = re.search(r'```python\s*\n(.*?)\n```', task, re.DOTALL)
            if match:
                return {"code": match.group(1).strip()}

            # Look for inline code
            match = re.search(r'`([^`]+)`', task)
            if match:
                return {"code": match.group(1).strip()}

            return {"code": ""}

        elif tool_name == "search":
            # Extract search query
            match = re.search(r'(?:search for|find|look up)\s+(.+?)(?:\.|$)', task, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
            else:
                # Use the whole task as query
                query = task[:100]  # Limit length

            return {"query": query, "max_results": 5}

        elif tool_name == "web_scrape":
            # Extract URL
            match = re.search(r'(https?://[^\s]+)', task)
            if match:
                return {"url": match.group(1)}

            return {"url": ""}

        return {}

    async def _execute_tool_with_params(
        self,
        tool_name: str,
        parameters: dict[str, Any],
    ) -> ToolResult:
        """Execute a tool with given parameters.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        self._add_thought(f"Executing {tool_name} with parameters: {parameters}")

        try:
            result = await self.tool_registry.execute_tool(tool_name, **parameters)

            if result.success:
                self._add_thought(f"Tool {tool_name} executed successfully")
            else:
                self._add_thought(f"Tool {tool_name} failed: {result.error}")

            return result

        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return ToolResult(
                success=False,
                result=None,
                error=str(e),
            )

    async def process(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResponse:
        """Process input with tool usage.

        Args:
            input_text: User input
            context: Additional context

        Returns:
            Agent response with tool results
        """
        self._add_thought(f"Analyzing task for tool usage: {input_text[:100]}...")

        # Step 1: Analyze tool needs
        tool_analysis = self._analyze_tool_needs(input_text, context)
        self._add_thought(f"Tool analysis: {tool_analysis['analysis']}")

        actions = []
        tool_results = []

        # Step 2: Execute tools if needed
        if tool_analysis["needs_tools"]:
            for tool_info in tool_analysis["tools"]:
                tool_name = tool_info["tool"]

                # Skip RAG retriever as it's handled separately
                if tool_name == "rag_retriever":
                    continue

                # Extract parameters
                parameters = self._extract_tool_parameters(input_text, tool_name)

                if not parameters or (
                    tool_name == "calculator" and not parameters.get("expression")
                ):
                    self._add_thought(f"Could not extract parameters for {tool_name}, skipping")
                    continue

                # Execute tool
                result = await self._execute_tool_with_params(tool_name, parameters)

                # Record action
                action = AgentAction(
                    action_type=f"tool_{tool_name}",
                    parameters=parameters,
                    result=result.result if result.success else result.error,
                )
                actions.append(action)
                tool_results.append({
                    "tool": tool_name,
                    "success": result.success,
                    "result": result.result,
                    "error": result.error,
                })

        # Step 3: Synthesize response
        if tool_results:
            # Build response incorporating tool results
            response_parts = []

            for tr in tool_results:
                if tr["success"]:
                    response_parts.append(f"Tool '{tr['tool']}' result: {tr['result']}")
                else:
                    response_parts.append(f"Tool '{tr['tool']}' error: {tr['error']}")

            # Use LLM to create coherent response
            synthesis_prompt = f"""Task: {input_text}

Tool Results:
{chr(10).join(response_parts)}

Based on these tool results, provide a clear, helpful response to the original task.
Explain the results in a user-friendly way."""

            final_response = await self._generate(synthesis_prompt)
            self._add_thought("Synthesized response from tool results")
        else:
            # No tools used, provide direct response
            self._add_thought("No tools needed for this task")
            final_response = await self._generate(input_text)

        return AgentResponse(
            content=final_response,
            thoughts=self.get_thoughts(),
            actions=actions,
            confidence=0.85 if tool_results else 0.7,
            metadata={
                "tools_used": [tr["tool"] for tr in tool_results],
                "tool_count": len(tool_results),
                "tool_analysis": tool_analysis,
            },
        )
