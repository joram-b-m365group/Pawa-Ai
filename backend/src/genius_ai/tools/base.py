"""Base tool interface for function calling."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable
from enum import Enum

from genius_ai.core.logger import logger


class ToolCategory(str, Enum):
    """Tool categories."""

    COMPUTATION = "computation"
    SEARCH = "search"
    FILE_OPERATION = "file_operation"
    WEB = "web"
    CODE_EXECUTION = "code_execution"
    DATA_ANALYSIS = "data_analysis"


@dataclass
class ToolParameter:
    """Tool parameter definition."""

    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


@dataclass
class ToolDefinition:
    """Tool definition for function calling."""

    name: str
    description: str
    parameters: list[ToolParameter]
    category: ToolCategory
    returns: str


@dataclass
class ToolResult:
    """Result from tool execution."""

    success: bool
    result: Any
    error: str | None = None
    metadata: dict[str, Any] | None = None


class BaseTool(ABC):
    """Abstract base class for tools."""

    def __init__(self):
        """Initialize tool."""
        self.definition = self._get_definition()

    @abstractmethod
    def _get_definition(self) -> ToolDefinition:
        """Get tool definition."""
        pass

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool.

        Args:
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        pass

    def get_schema(self) -> dict[str, Any]:
        """Get tool schema for function calling.

        Returns:
            OpenAI-style function schema
        """
        properties = {}
        required = []

        for param in self.definition.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.default is not None:
                properties[param.name]["default"] = param.default

            if param.required:
                required.append(param.name)

        return {
            "name": self.definition.name,
            "description": self.definition.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }


class CalculatorTool(BaseTool):
    """Tool for mathematical calculations."""

    def _get_definition(self) -> ToolDefinition:
        """Get tool definition."""
        return ToolDefinition(
            name="calculator",
            description="Perform mathematical calculations. Supports basic arithmetic and mathematical functions.",
            parameters=[
                ToolParameter(
                    name="expression",
                    type="string",
                    description="Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)')",
                ),
            ],
            category=ToolCategory.COMPUTATION,
            returns="Result of the calculation",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute calculation."""
        try:
            expression = kwargs.get("expression", "")

            # Safe evaluation (limited scope)
            import math
            import operator

            # Allowed operations
            allowed_names = {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
                # Math functions
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
            }

            # Evaluate expression
            result = eval(expression, {"__builtins__": {}}, allowed_names)

            logger.info(f"Calculator: {expression} = {result}")

            return ToolResult(
                success=True,
                result=result,
                metadata={"expression": expression},
            )

        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return ToolResult(
                success=False,
                result=None,
                error=str(e),
            )


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        """Initialize tool registry."""
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool to register
        """
        self._tools[tool.definition.name] = tool
        logger.info(f"Registered tool: {tool.definition.name}")

    def get_tool(self, name: str) -> BaseTool | None:
        """Get tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None
        """
        return self._tools.get(name)

    def get_all_tools(self) -> list[BaseTool]:
        """Get all registered tools.

        Returns:
            List of tools
        """
        return list(self._tools.values())

    def get_schemas(self) -> list[dict[str, Any]]:
        """Get schemas for all tools.

        Returns:
            List of tool schemas
        """
        return [tool.get_schema() for tool in self._tools.values()]

    async def execute_tool(self, name: str, **kwargs: Any) -> ToolResult:
        """Execute a tool by name.

        Args:
            name: Tool name
            **kwargs: Tool parameters

        Returns:
            Tool result
        """
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                success=False,
                result=None,
                error=f"Tool '{name}' not found",
            )

        return await tool.execute(**kwargs)


class SearchTool(BaseTool):
    """Tool for searching information (simulated)."""

    def _get_definition(self) -> ToolDefinition:
        """Get tool definition."""
        return ToolDefinition(
            name="search",
            description="Search for information on a given topic. Returns relevant information.",
            parameters=[
                ToolParameter(
                    name="query",
                    type="string",
                    description="Search query",
                ),
                ToolParameter(
                    name="max_results",
                    type="integer",
                    description="Maximum number of results to return",
                    required=False,
                    default=5,
                ),
            ],
            category=ToolCategory.SEARCH,
            returns="Search results with relevant information",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute search.

        Note: This is a placeholder. In production, integrate with actual search API
        (e.g., Google Custom Search, Bing API, or internal knowledge base).
        """
        try:
            query = kwargs.get("query", "")
            max_results = kwargs.get("max_results", 5)

            logger.info(f"Search: {query} (max {max_results} results)")

            # Placeholder response
            result = {
                "query": query,
                "message": "Search tool placeholder - integrate with actual search API",
                "suggestion": "Use RAG retriever for knowledge base search",
            }

            return ToolResult(
                success=True,
                result=result,
                metadata={"query": query, "max_results": max_results},
            )

        except Exception as e:
            logger.error(f"Search error: {e}")
            return ToolResult(
                success=False,
                result=None,
                error=str(e),
            )


class CodeExecutionTool(BaseTool):
    """Tool for safe code execution (Python)."""

    def _get_definition(self) -> ToolDefinition:
        """Get tool definition."""
        return ToolDefinition(
            name="execute_code",
            description="Execute Python code safely in a restricted environment. Use for data analysis, calculations, or testing code.",
            parameters=[
                ToolParameter(
                    name="code",
                    type="string",
                    description="Python code to execute",
                ),
                ToolParameter(
                    name="timeout",
                    type="integer",
                    description="Execution timeout in seconds",
                    required=False,
                    default=5,
                ),
            ],
            category=ToolCategory.CODE_EXECUTION,
            returns="Code execution result or error",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute code safely."""
        try:
            code = kwargs.get("code", "")
            timeout = kwargs.get("timeout", 5)

            logger.info(f"Executing code (timeout: {timeout}s)")

            # Create restricted globals with safe builtins
            import math
            import datetime
            import json

            safe_globals = {
                "__builtins__": {
                    # Safe built-ins
                    "abs": abs,
                    "all": all,
                    "any": any,
                    "bool": bool,
                    "dict": dict,
                    "enumerate": enumerate,
                    "filter": filter,
                    "float": float,
                    "int": int,
                    "len": len,
                    "list": list,
                    "map": map,
                    "max": max,
                    "min": min,
                    "range": range,
                    "round": round,
                    "set": set,
                    "sorted": sorted,
                    "str": str,
                    "sum": sum,
                    "tuple": tuple,
                    "zip": zip,
                    "print": print,
                },
                "math": math,
                "datetime": datetime,
                "json": json,
            }

            # Create local namespace for execution
            local_namespace = {}

            # Execute code
            exec(code, safe_globals, local_namespace)

            # Capture any output or return value
            result = {
                "status": "success",
                "namespace": {k: str(v) for k, v in local_namespace.items() if not k.startswith("_")},
            }

            logger.info(f"Code executed successfully")

            return ToolResult(
                success=True,
                result=result,
                metadata={"code_length": len(code)},
            )

        except Exception as e:
            logger.error(f"Code execution error: {e}")
            return ToolResult(
                success=False,
                result=None,
                error=f"Execution failed: {str(e)}",
            )


class WebScrapeTool(BaseTool):
    """Tool for web scraping (placeholder)."""

    def _get_definition(self) -> ToolDefinition:
        """Get tool definition."""
        return ToolDefinition(
            name="web_scrape",
            description="Fetch and extract content from a web URL.",
            parameters=[
                ToolParameter(
                    name="url",
                    type="string",
                    description="URL to scrape",
                ),
            ],
            category=ToolCategory.WEB,
            returns="Extracted web content",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute web scraping.

        Note: Placeholder for actual web scraping implementation.
        """
        try:
            url = kwargs.get("url", "")

            logger.info(f"Web scrape: {url}")

            # Placeholder response
            result = {
                "url": url,
                "message": "Web scraping tool placeholder",
                "suggestion": "Integrate with libraries like BeautifulSoup or Scrapy",
            }

            return ToolResult(
                success=True,
                result=result,
                metadata={"url": url},
            )

        except Exception as e:
            logger.error(f"Web scrape error: {e}")
            return ToolResult(
                success=False,
                result=None,
                error=str(e),
            )


# Global tool registry
tool_registry = ToolRegistry()

# Register default tools
tool_registry.register(CalculatorTool())
tool_registry.register(SearchTool())
tool_registry.register(CodeExecutionTool())
tool_registry.register(WebScrapeTool())
