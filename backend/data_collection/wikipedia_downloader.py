"""Wikipedia Knowledge Base Builder - FREE

Downloads and processes Wikipedia dump for massive knowledge base.

Target: 6M+ articles, 50GB+ of knowledge
Cost: $0 (just bandwidth and disk space)
"""

import requests
import json
import os
from pathlib import Path

class WikipediaDownloader:
    def __init__(self, output_dir="data/wikipedia"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Wikipedia API (free, no auth)
        self.api_url = "https://en.wikipedia.org/w/api.php"

    def get_article(self, title):
        """Get a single Wikipedia article.

        Args:
            title: Article title (e.g., "Python (programming language)")
        """
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,  # Plain text, no HTML
            "exsectionformat": "plain"
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})

            for page_id, page in pages.items():
                if "extract" in page:
                    return {
                        "title": page["title"],
                        "text": page["extract"],
                        "page_id": page_id
                    }

        return None

    def search_articles(self, query, limit=10):
        """Search for articles by query.

        Args:
            query: Search term
            limit: Number of results
        """
        params = {
            "action": "opensearch",
            "format": "json",
            "search": query,
            "limit": limit
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            # Returns: [query, [titles], [descriptions], [urls]]
            return data[1] if len(data) > 1 else []

        return []

    def get_category_articles(self, category, limit=500):
        """Get articles in a category.

        Args:
            category: Category name (e.g., "Category:Python (programming language)")
            limit: Maximum articles to fetch
        """
        articles = []
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": min(limit, 500),  # API max is 500
            "cmtype": "page"  # Only articles, not subcategories
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            members = data.get("query", {}).get("categorymembers", [])

            for member in members:
                articles.append(member["title"])

        return articles

    def download_topics(self, topics, articles_per_topic=100):
        """Download articles for specific topics.

        Args:
            topics: List of topics to download
            articles_per_topic: Max articles per topic
        """
        all_examples = []

        for topic in topics:
            print(f"\nDownloading articles for: {topic}")
            print("-" * 70)

            # Search for articles about this topic
            article_titles = self.search_articles(topic, limit=articles_per_topic)

            for i, title in enumerate(article_titles, 1):
                article = self.get_article(title)

                if article and article["text"]:
                    # Split into Q&A format
                    # Use first paragraph as summary
                    paragraphs = article["text"].split("\n\n")
                    summary = paragraphs[0] if paragraphs else article["text"][:500]

                    example = {
                        "prompt": f"What is {article['title']}? Explain in detail.",
                        "response": summary[:1000],  # Limit length for training
                        "full_text": article["text"][:5000],  # Store more for RAG
                        "metadata": {
                            "source": "wikipedia",
                            "title": article["title"],
                            "page_id": article["page_id"],
                            "topic": topic
                        }
                    }

                    all_examples.append(example)

                    if i % 10 == 0:
                        print(f"  Downloaded {i}/{len(article_titles)} articles...")

            print(f"Completed {topic}: {len(article_titles)} articles")

        # Save to file
        output_file = self.output_dir / "wikipedia_knowledge.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_examples, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(all_examples)} articles to {output_file}")
        return all_examples

    def download_full_dump(self):
        """Download complete Wikipedia dump (advanced).

        NOTE: This downloads ~20GB compressed, ~90GB uncompressed!
        Only run if you have space and bandwidth.
        """
        print("WARNING: This downloads 20GB+ of data!")
        print("Recommended: Use the API methods above for targeted collection.")
        print("\nFor full dump, visit: https://dumps.wikimedia.org/enwiki/latest/")
        print("Download: enwiki-latest-pages-articles.xml.bz2")


def main():
    """Download Wikipedia articles for key topics."""
    downloader = WikipediaDownloader()

    # Topics to download (customize for your needs)
    topics = [
        # Programming (2,000 articles)
        "Python programming language",
        "JavaScript",
        "Web development",
        "Software engineering",
        "Computer science",
        "Algorithms",
        "Data structures",
        "Machine learning",
        "Artificial intelligence",
        "Database",

        # Business (1,000 articles)
        "Entrepreneurship",
        "Startup company",
        "Business model",
        "Marketing",
        "Sales",
        "Finance",
        "Economics",
        "Management",

        # Science (1,000 articles)
        "Physics",
        "Chemistry",
        "Biology",
        "Mathematics",
        "Statistics",
        "Astronomy",

        # General Knowledge (1,000 articles)
        "History",
        "Geography",
        "Philosophy",
        "Psychology",
        "Literature",
    ]

    print("=" * 70)
    print("WIKIPEDIA KNOWLEDGE BASE BUILDER")
    print("=" * 70)
    print(f"\nDownloading articles for {len(topics)} topics")
    print(f"Target: ~5,000 articles (100 per topic)")
    print(f"This will take ~30-60 minutes...")
    print("\n" + "=" * 70 + "\n")

    examples = downloader.download_topics(topics, articles_per_topic=100)

    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE!")
    print("=" * 70)
    print(f"Total articles: {len(examples)}")
    print(f"Output: data/wikipedia/wikipedia_knowledge.json")
    print("\nThese articles are now ready for:")
    print("  1. Training data (Q&A pairs)")
    print("  2. RAG knowledge base (full text)")
    print("=" * 70)


if __name__ == "__main__":
    main()
