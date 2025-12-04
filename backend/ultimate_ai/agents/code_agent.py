"""
Code Master Agent
Handles programming, coding, technical questions
"""

from typing import Optional, Dict
import re
from .base_agent import BaseAgent, AgentResponse


class CodeAgent(BaseAgent):
    """
    Expert in programming, software development, debugging
    """

    def __init__(self, core_intelligence):
        super().__init__("CodeAgent", core_intelligence)
        self.expertise_keywords = [
            "code", "program", "function", "class", "debug", "error",
            "python", "javascript", "java", "c++", "algorithm",
            "api", "database", "framework", "library", "package",
            "bug", "syntax", "compile", "runtime", "implement"
        ]

        # Programming language keywords
        self.languages = [
            "python", "javascript", "java", "c++", "c#", "ruby", "go",
            "rust", "php", "swift", "kotlin", "typescript", "sql",
            "html", "css", "react", "vue", "angular", "node"
        ]

    async def can_handle(self, message: str) -> float:
        """
        Check if this is a coding question
        """
        msg_lower = message.lower()

        # Check for code blocks
        if "```" in message or re.search(r'`[^`]+`', message):
            return 0.98

        # Check for programming language mentions
        if any(lang in msg_lower for lang in self.languages):
            return 0.95

        # Check for coding phrases
        coding_phrases = [
            "write a function", "create a program", "how do i code",
            "implement", "algorithm for", "code to", "script that",
            "fix this error", "debug", "why isn't this working"
        ]

        if any(phrase in msg_lower for phrase in coding_phrases):
            return 0.95

        # Standard keyword matching
        confidence = self._calculate_keyword_confidence(message)

        return confidence

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process coding question

        Handles:
        - Writing code
        - Debugging
        - Explaining code
        - Algorithm design
        - Best practices
        """
        system_prompt = """You are a master programmer and software engineer. When helping with code:

1. **Understand the requirement**: What does the user want to achieve?
2. **Write clean code**: Follow best practices, use clear variable names
3. **Explain your code**: Add comments, explain logic
4. **Consider edge cases**: Handle errors, validate input
5. **Provide examples**: Show how to use the code
6. **Suggest improvements**: Optimization, readability, security

Write production-quality code with explanations. Be a helpful coding mentor."""

        # Detect if user is asking for code to be written
        msg_lower = message.lower()
        is_code_request = any(phrase in msg_lower for phrase in [
            "write", "create", "make", "implement", "build", "code for"
        ])

        if is_code_request:
            # Code generation mode
            prompt = f"""{system_prompt}

**Task**: {message}

**Please provide:**
1. Clean, working code
2. Explanation of how it works
3. Example usage
4. Any important notes or considerations

**Code:**"""
        else:
            # Code explanation/debugging mode
            prompt = f"""{system_prompt}

**Question**: {message}

**Please provide:**
1. Clear explanation
2. Code examples if helpful
3. Best practices
4. Common pitfalls to avoid

**Answer:**"""

        # Generate code/explanation
        response = await self.core.generate(
            prompt,
            temperature=0.4  # Balanced for code - not too random, not too rigid
        )

        # Detect programming language used
        detected_lang = None
        for lang in self.languages:
            if lang in msg_lower:
                detected_lang = lang
                break

        return AgentResponse(
            content=response,
            confidence=0.9,
            agent_name=self.name,
            reasoning="Used programming expertise and best practices",
            metadata={
                "type": "code_generation" if is_code_request else "code_help",
                "language": detected_lang
            }
        )
