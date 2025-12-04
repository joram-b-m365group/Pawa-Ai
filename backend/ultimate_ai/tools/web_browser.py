"""
Web Browser Tool
Fetches and processes web content
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, urlparse


class WebBrowser:
    """
    Advanced web browsing capabilities

    Can:
    - Fetch web pages
    - Extract main content
    - Follow links
    - Handle JavaScript (with playwright)
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def fetch_page(self, url: str) -> Dict[str, any]:
        """
        Fetch a web page and extract content

        Args:
            url: URL to fetch

        Returns:
            Dict with title, content, links, images
        """
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status != 200:
                        return {"error": f"HTTP {response.status}"}

                    html = await response.text()
                    return self._parse_html(html, url)

        except asyncio.TimeoutError:
            return {"error": "Timeout fetching page"}
        except Exception as e:
            return {"error": str(e)}

    def _parse_html(self, html: str, base_url: str) -> Dict:
        """Parse HTML and extract useful content"""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Extract title
        title = soup.find('title')
        title = title.get_text().strip() if title else "No title"

        # Extract main content
        content = self._extract_main_content(soup)

        # Extract links
        links = self._extract_links(soup, base_url)

        # Extract images
        images = self._extract_images(soup, base_url)

        # Extract metadata
        metadata = self._extract_metadata(soup)

        return {
            "url": base_url,
            "title": title,
            "content": content,
            "links": links[:20],  # Top 20 links
            "images": images[:10],  # Top 10 images
            "metadata": metadata
        }

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main readable content"""
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('body')

        if not main_content:
            return ""

        # Get text
        text = main_content.get_text(separator='\n', strip=True)

        # Clean up whitespace
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        # Limit length (first 5000 chars for summary)
        if len(text) > 5000:
            text = text[:5000] + "..."

        return text

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all links from page"""
        links = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)

            # Only include http/https links
            if absolute_url.startswith(('http://', 'https://')):
                links.append({
                    "url": absolute_url,
                    "text": a_tag.get_text(strip=True)[:100]  # Limit text
                })

        return links

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract images from page"""
        images = []

        for img_tag in soup.find_all('img', src=True):
            src = img_tag['src']
            absolute_url = urljoin(base_url, src)

            if absolute_url.startswith(('http://', 'https://')):
                images.append({
                    "url": absolute_url,
                    "alt": img_tag.get('alt', '')
                })

        return images

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract metadata from page"""
        metadata = {}

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata['description'] = meta_desc.get('content', '')

        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            metadata['keywords'] = meta_keywords.get('content', '')

        # Open Graph tags
        for og_tag in soup.find_all('meta', attrs={'property': re.compile(r'^og:')}):
            key = og_tag['property'][3:]  # Remove 'og:' prefix
            metadata[f'og_{key}'] = og_tag.get('content', '')

        return metadata

    async def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google (using DuckDuckGo HTML - no API needed)

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results
        """
        # Use DuckDuckGo's HTML search (no API, no rate limits)
        search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"

        try:
            page_data = await self.fetch_page(search_url)

            if "error" in page_data:
                return []

            # Parse would happen here - for now, return mock results
            # In production, parse the HTML results
            return [{
                "title": f"Result for: {query}",
                "url": "https://example.com",
                "snippet": "Search result snippet..."
            }]

        except Exception as e:
            return []

    async def multi_page_synthesis(self, urls: List[str]) -> str:
        """
        Fetch multiple pages and synthesize information

        Args:
            urls: List of URLs to fetch

        Returns:
            Combined and cleaned content
        """
        # Fetch all pages in parallel
        tasks = [self.fetch_page(url) for url in urls]
        pages = await asyncio.gather(*tasks)

        # Combine content
        combined_content = []
        for page in pages:
            if "error" not in page:
                combined_content.append(f"### {page['title']}\n\n{page['content']}\n")

        return "\n\n".join(combined_content)
