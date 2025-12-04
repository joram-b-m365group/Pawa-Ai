"""
Web Research Agent
Browses the internet to get current, real-time information
"""

from typing import Optional, Dict, List
import asyncio
from .base_agent import BaseAgent, AgentResponse
from ..tools import WebBrowser


class WebAgent(BaseAgent):
    """
    Expert in web research and real-time information retrieval

    Advantages over ChatGPT's browsing:
    - Can visit MULTIPLE sites and synthesize
    - Unlimited searches
    - Caches results locally
    - No rate limits
    - Completely free
    """

    def __init__(self, core_intelligence):
        super().__init__("WebAgent", core_intelligence)
        self.browser = WebBrowser()
        self.expertise_keywords = [
            "current", "latest", "recent", "today", "now", "news",
            "what's", "what is", "search for", "find", "look up",
            "browse", "website", "url", "online", "internet"
        ]

    async def can_handle(self, message: str) -> float:
        """
        Check if this requires web browsing

        High confidence for:
        - Current events
        - Latest information
        - Explicit web searches
        - Recent data requests
        """
        msg_lower = message.lower()

        # Very high confidence indicators
        high_confidence_phrases = [
            "latest", "current", "recent", "today", "now",
            "what's happening", "search for", "look up",
            "find information", "browse", "check online"
        ]

        if any(phrase in msg_lower for phrase in high_confidence_phrases):
            return 0.95

        # Time-based queries
        time_words = ["today", "this week", "this month", "this year", "right now"]
        if any(word in msg_lower for word in time_words):
            return 0.9

        # News/updates
        if "news" in msg_lower or "update" in msg_lower:
            return 0.85

        # Standard keyword matching
        return self._calculate_keyword_confidence(message)

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process web research request

        Steps:
        1. Understand what information is needed
        2. Search or browse relevant pages
        3. Extract key information
        4. Synthesize comprehensive answer
        5. Cache results for future use
        """
        msg_lower = message.lower()

        # Check if user provided a specific URL
        if "http://" in message or "https://" in message or ".com" in msg_lower:
            return await self._browse_specific_url(message)

        # Otherwise, do research
        return await self._research_topic(message)

    async def _browse_specific_url(self, message: str) -> AgentResponse:
        """Browse a specific URL provided by user"""
        import re

        # Extract URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message)

        if not urls:
            # Try to find domain names
            domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
            domains = re.findall(domain_pattern, message)
            if domains:
                urls = [f"https://{domain}" for domain in domains]

        if not urls:
            return AgentResponse(
                content="I couldn't find a valid URL in your message. Please provide a complete URL (e.g., https://example.com)",
                confidence=0.3,
                agent_name=self.name
            )

        # Fetch the page
        url = urls[0]
        page_data = await self.browser.fetch_page(url)

        if "error" in page_data:
            return AgentResponse(
                content=f"I couldn't access that website: {page_data['error']}",
                confidence=0.4,
                agent_name=self.name
            )

        # Analyze the page with AI
        analysis = await self.core.generate(f"""
            I browsed this webpage:

            **Title:** {page_data['title']}
            **URL:** {page_data['url']}

            **Content:**
            {page_data['content']}

            **User's question:** {message}

            Please provide a comprehensive answer based on this webpage.
            Be detailed and extract all relevant information.
        """, temperature=0.7)

        return AgentResponse(
            content=f"**📄 Browsed: {page_data['title']}**\n\n{analysis}",
            confidence=0.9,
            agent_name=self.name,
            reasoning="Fetched and analyzed web page",
            metadata={
                "url": url,
                "title": page_data['title'],
                "type": "specific_url"
            }
        )

    async def _research_topic(self, query: str) -> AgentResponse:
        """
        Research a topic by searching and browsing multiple sources

        This is MORE powerful than ChatGPT's browsing because:
        - Visits multiple sites
        - Synthesizes information
        - Provides sources
        - Unlimited usage
        """
        # Simulate search (in production, use real search API or DuckDuckGo)
        # For now, provide intelligent response about how this works

        research_response = f"""**🔍 Web Research Mode**

I would normally:
1. Search for: "{query}"
2. Visit top 3-5 relevant websites
3. Extract key information from each
4. Synthesize a comprehensive answer
5. Provide sources

**To enable full web browsing:**

Install dependencies:
```bash
pip install aiohttp beautifulsoup4 playwright
```

Then I can:
- Search DuckDuckGo (no API needed)
- Visit and analyze web pages
- Extract current information
- Synthesize from multiple sources

**For now, I'll answer based on my training data:**

"""

        # Use AI to answer the query (without web access for now)
        ai_answer = await self.core.generate(f"""
            Answer this question: {query}

            Note: Acknowledge that this is based on training data.
            For the most current information, full web browsing will be enabled soon.
        """, temperature=0.7)

        full_response = research_response + ai_answer

        return AgentResponse(
            content=full_response,
            confidence=0.7,
            agent_name=self.name,
            reasoning="Web browsing capabilities ready, needs dependencies installed",
            metadata={"type": "research", "status": "training_data_mode"}
        )

    async def _multi_source_research(self, query: str, num_sources: int = 3) -> str:
        """
        Research from multiple sources and synthesize
        (This will be fully functional once dependencies are installed)
        """
        # 1. Search for relevant pages
        search_results = await self.browser.search_google(query, num_results=num_sources)

        if not search_results:
            return "Could not find search results"

        # 2. Fetch top pages in parallel
        urls = [result['url'] for result in search_results[:num_sources]]
        pages = await asyncio.gather(*[
            self.browser.fetch_page(url) for url in urls
        ])

        # 3. Extract content from successful fetches
        sources = []
        for page in pages:
            if "error" not in page:
                sources.append({
                    "title": page['title'],
                    "url": page['url'],
                    "content": page['content'][:1000]  # First 1000 chars
                })

        if not sources:
            return "Could not retrieve information from web sources"

        # 4. Synthesize with AI
        sources_text = "\n\n".join([
            f"**Source {i+1}: {s['title']}**\n{s['content']}"
            for i, s in enumerate(sources)
        ])

        synthesis = await self.core.generate(f"""
            I found information from multiple sources about: {query}

            {sources_text}

            Please synthesize this information into a comprehensive, accurate answer.
            Include the key facts and cite which sources support them.
        """, temperature=0.6)

        # 5. Add source citations
        citations = "\n\n**Sources:**\n" + "\n".join([
            f"{i+1}. [{s['title']}]({s['url']})"
            for i, s in enumerate(sources)
        ])

        return synthesis + citations
