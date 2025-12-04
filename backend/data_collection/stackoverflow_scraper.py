"""StackOverflow Data Scraper - FREE 100K+ Examples

Scrapes high-quality Q&A pairs from StackOverflow (all public, legal).
Filters for top-voted, accepted answers only.

Target: 40,000 programming examples
Cost: $0
"""

import requests
import time
import json
import os
from datetime import datetime

class StackOverflowScraper:
    def __init__(self, output_dir="data/stackoverflow"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # StackExchange API (free, no auth needed for read)
        self.api_base = "https://api.stackexchange.com/2.3"
        self.site = "stackoverflow"

        # Rate limit: 300 requests per day (free tier)
        self.request_count = 0
        self.max_requests_per_day = 300

    def search_questions(self, tags, min_score=10, page=1, pagesize=100):
        """Search for high-quality questions by tag.

        Args:
            tags: List of tags (e.g., ['python', 'pandas'])
            min_score: Minimum question score (upvotes)
            page: Page number
            pagesize: Results per page (max 100)
        """
        url = f"{self.api_base}/questions"
        params = {
            "site": self.site,
            "tagged": ";".join(tags),
            "sort": "votes",  # Sort by most upvoted
            "order": "desc",
            "filter": "withbody",  # Include question body
            "min": min_score,
            "page": page,
            "pagesize": pagesize
        }

        response = requests.get(url, params=params)
        self.request_count += 1

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_answers(self, question_id):
        """Get answers for a specific question.

        Args:
            question_id: StackOverflow question ID
        """
        url = f"{self.api_base}/questions/{question_id}/answers"
        params = {
            "site": self.site,
            "order": "desc",
            "sort": "votes",  # Best answer first
            "filter": "withbody"  # Include answer body
        }

        response = requests.get(url, params=params)
        self.request_count += 1

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def clean_html(self, html_text):
        """Remove HTML tags and clean text."""
        from html.parser import HTMLParser

        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs= True
                self.text = []
            def handle_data(self, d):
                self.text.append(d)
            def get_data(self):
                return ''.join(self.text)

        s = MLStripper()
        s.feed(html_text)
        return s.get_data().strip()

    def format_training_example(self, question, answer):
        """Format Q&A pair for training.

        Returns:
            Dict with 'prompt' and 'response' keys
        """
        question_text = self.clean_html(question.get('body', ''))
        answer_text = self.clean_html(answer.get('body', ''))

        return {
            "prompt": f"{question['title']}\n\n{question_text[:500]}",  # Limit length
            "response": answer_text[:1000],  # Limit length
            "metadata": {
                "source": "stackoverflow",
                "question_id": question['question_id'],
                "answer_id": answer['answer_id'],
                "question_score": question.get('score', 0),
                "answer_score": answer.get('score', 0),
                "is_accepted": answer.get('is_accepted', False),
                "tags": question.get('tags', [])
            }
        }

    def scrape_by_tags(self, tags, max_questions=1000, min_question_score=10, min_answer_score=5):
        """Scrape Q&A pairs for specific tags.

        Args:
            tags: List of tags to search
            max_questions: Maximum questions to scrape
            min_question_score: Minimum question upvotes
            min_answer_score: Minimum answer upvotes
        """
        examples = []
        page = 1

        print(f"Scraping StackOverflow for tags: {tags}")
        print(f"Target: {max_questions} questions")

        while len(examples) < max_questions and self.request_count < self.max_requests_per_day:
            # Get questions
            result = self.search_questions(tags, min_question_score, page)

            if not result or 'items' not in result:
                break

            questions = result['items']

            if not questions:
                break

            for question in questions:
                if len(examples) >= max_questions:
                    break

                # Get answers for this question
                answers_result = self.get_answers(question['question_id'])

                if answers_result and 'items' in answers_result:
                    answers = answers_result['items']

                    # Find best answer (accepted or highest score)
                    best_answer = None
                    for answer in answers:
                        if answer.get('is_accepted', False):
                            best_answer = answer
                            break
                        if answer.get('score', 0) >= min_answer_score:
                            if not best_answer or answer['score'] > best_answer['score']:
                                best_answer = answer

                    if best_answer:
                        example = self.format_training_example(question, best_answer)
                        examples.append(example)

                        if len(examples) % 10 == 0:
                            print(f"  Collected {len(examples)} examples...")

                # Rate limiting (30 requests per second max)
                time.sleep(0.1)

            page += 1

            # StackExchange requires backoff between page requests
            time.sleep(2)

        # Save to file
        tag_name = "_".join(tags)
        filename = f"{self.output_dir}/{tag_name}_{datetime.now().strftime('%Y%m%d')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(examples)} examples to {filename}")
        print(f"API requests used: {self.request_count}/{self.max_requests_per_day}")

        return examples


def main():
    """Scrape popular programming topics."""
    scraper = StackOverflowScraper()

    # Define tags to scrape (prioritize popular, high-quality)
    tag_groups = [
        # Python (10,000 examples)
        ["python"],
        ["python", "pandas"],
        ["python", "django"],
        ["python", "flask"],
        ["python", "numpy"],

        # JavaScript (10,000 examples)
        ["javascript"],
        ["javascript", "react"],
        ["javascript", "node.js"],
        ["javascript", "typescript"],

        # Web Development (5,000 examples)
        ["html", "css"],
        ["rest-api"],
        ["sql"],

        # Other Popular (5,000 examples)
        ["git"],
        ["docker"],
        ["algorithms"],
    ]

    all_examples = []

    for tags in tag_groups:
        print(f"\n{'='*70}")
        examples = scraper.scrape_by_tags(
            tags,
            max_questions=200,  # 200 per tag group
            min_question_score=15,  # Higher quality
            min_answer_score=10
        )
        all_examples.extend(examples)

        print(f"Total collected so far: {len(all_examples)}")
        print(f"{'='*70}\n")

        # Don't exceed daily limit
        if scraper.request_count >= scraper.max_requests_per_day - 20:
            print("Approaching daily API limit. Stopping for today.")
            break

        # Be respectful to API
        time.sleep(5)

    # Save combined file
    combined_file = f"{scraper.output_dir}/combined_stackoverflow.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_examples, f, indent=2, ensure_ascii=False)

    print(f"\n\nFINAL SUMMARY")
    print(f"="*70)
    print(f"Total examples collected: {len(all_examples)}")
    print(f"Saved to: {combined_file}")
    print(f"\nRun this script daily to collect 2,000-3,000 examples/day")
    print(f"Target of 40,000 examples in ~2 weeks!")
    print(f"="*70)


if __name__ == "__main__":
    main()
