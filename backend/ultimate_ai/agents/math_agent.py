"""
Mathematical Genius Agent
Handles math, calculations, problem-solving
"""

import ast
import operator
import math
import re
from typing import Optional, Dict, Any
from .base_agent import BaseAgent, AgentResponse


class MathAgent(BaseAgent):
    """
    Expert in mathematics - from basic arithmetic to advanced calculus
    """

    def __init__(self, core_intelligence):
        super().__init__("MathAgent", core_intelligence)
        self.expertise_keywords = [
            "calculate", "solve", "math", "equation", "formula",
            "add", "subtract", "multiply", "divide", "sum", "product",
            "derivative", "integral", "calculus", "algebra", "geometry",
            "trigonometry", "statistics", "probability", "matrix"
        ]

        # Safe operators for evaluation
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

    async def can_handle(self, message: str) -> float:
        """
        Check if this is a math question
        """
        msg_lower = message.lower()

        # Check for explicit math expressions (numbers with operators)
        if re.search(r'\d+\s*[\+\-\*\/\^]\s*\d+', message):
            return 0.98

        # Check for math keywords
        math_phrases = [
            "calculate", "what is", "solve", "how much is",
            "what's", "compute", "find the", "determine"
        ]
        if any(phrase in msg_lower for phrase in math_phrases):
            # Check if numbers are involved
            if re.search(r'\d+', message):
                return 0.95

        # Standard keyword matching
        confidence = self._calculate_keyword_confidence(message)

        # Boost confidence if numbers are present
        if confidence > 0 and re.search(r'\d+', message):
            confidence = min(0.95, confidence + 0.3)

        return confidence

    def _safe_eval_math(self, expr: str) -> Any:
        """
        Safely evaluate mathematical expressions

        Args:
            expr: Mathematical expression as string

        Returns:
            Computed result
        """
        # Replace common math symbols
        expr = expr.replace('^', '**').replace('÷', '/').replace('×', '*')

        try:
            # Parse the expression
            node = ast.parse(expr, mode='eval')

            # Evaluate safely
            def eval_node(node):
                if isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.Num):  # Python 3.7 and earlier
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = eval_node(node.left)
                    right = eval_node(node.right)
                    return self.operators[type(node.op)](left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = eval_node(node.operand)
                    return self.operators[type(node.op)](operand)
                elif isinstance(node, ast.Call):
                    # Allow safe math functions
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if hasattr(math, func_name):
                            func = getattr(math, func_name)
                            args = [eval_node(arg) for arg in node.args]
                            return func(*args)
                raise ValueError(f"Unsupported operation: {type(node)}")

            result = eval_node(node.body)
            return result

        except Exception as e:
            raise ValueError(f"Cannot evaluate expression: {str(e)}")

    def _extract_math_expression(self, message: str) -> Optional[str]:
        """
        Extract mathematical expression from message

        Args:
            message: User's message

        Returns:
            Extracted expression or None
        """
        # Pattern for math expressions
        patterns = [
            r'(\d+\.?\d*\s*[\+\-\*\/\^÷×]\s*\d+\.?\d*(?:\s*[\+\-\*\/\^÷×]\s*\d+\.?\d*)*)',
            r'what\s+is\s+(\d+\.?\d*\s*[\+\-\*\/\^÷×]\s*\d+\.?\d*)',
            r'calculate\s+(\d+\.?\d*\s*[\+\-\*\/\^÷×]\s*\d+\.?\d*)',
            r'solve\s+(\d+\.?\d*\s*[\+\-\*\/\^÷×]\s*\d+\.?\d*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process mathematical question

        Can handle:
        - Arithmetic calculations
        - Algebraic equations
        - Word problems
        - Advanced mathematics
        """
        msg_lower = message.lower()

        # Try to extract and calculate simple expressions
        expr = self._extract_math_expression(message)

        if expr:
            try:
                result = self._safe_eval_math(expr)

                # Format result nicely
                if isinstance(result, float):
                    # Round to reasonable precision
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)

                response_text = f"**Calculation:**\n\n{expr} = **{result}**"

                # Add step-by-step for complex expressions
                if len(expr.split()) > 3:
                    response_text += f"\n\nLet me break this down:\n- Expression: {expr}\n- Result: {result}"

                return AgentResponse(
                    content=response_text,
                    confidence=0.99,
                    agent_name=self.name,
                    reasoning="Computed using symbolic mathematics engine",
                    metadata={"expression": expr, "result": result, "type": "calculation"}
                )

            except Exception as e:
                # If direct calculation fails, use AI to solve
                pass

        # For complex math problems, use AI reasoning
        system_prompt = """You are a mathematical genius. When solving math problems:

1. **Understand the problem**: Read carefully, identify what's being asked
2. **Show your work**: Explain each step clearly
3. **Use proper notation**: Mathematical symbols and formatting
4. **Verify your answer**: Check if it makes sense
5. **Explain the concept**: Help the user understand, don't just give answers

Solve problems step-by-step, explain your reasoning, and make math accessible."""

        # Generate mathematical solution
        full_prompt = f"{system_prompt}\n\nMathematics Problem: {message}\n\nSolution:"

        response = await self.core.generate(
            full_prompt,
            temperature=0.3  # Low temperature for accuracy
        )

        return AgentResponse(
            content=response,
            confidence=0.85,
            agent_name=self.name,
            reasoning="Used mathematical reasoning and problem-solving",
            metadata={"type": "problem_solving"}
        )
