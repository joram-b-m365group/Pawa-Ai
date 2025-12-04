"""
Simple RAG System for Genius AI - No Downloads Required
Uses TF-IDF for semantic search without heavy models
"""
import os
import sys
import glob
import json
from typing import List, Dict
from collections import defaultdict
import math
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

class SimpleRAGSystem:
    def __init__(self, guides_path: str = "../", index_path: str = "./rag_index.json"):
        """Initialize simple RAG system with TF-IDF"""
        print("🔧 Initializing Simple RAG System...")
        self.guides_path = guides_path
        self.index_path = index_path
        self.index = {
            'documents': [],
            'chunks': [],
            'tf_idf': {},
            'doc_count': 0
        }

        # Try to load existing index
        if os.path.exists(index_path):
            print("   Loading existing index...")
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                print(f"   ✅ Loaded {len(self.index['chunks'])} chunks from index")
            except Exception as e:
                print(f"   ⚠️  Could not load index: {e}")
                print("   Will create new index")

        print("✅ Simple RAG System initialized!\n")

    def preprocess_text(self, text: str) -> List[str]:
        """Convert text to lowercase and split into words"""
        # Remove special characters and convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        # Split into words
        words = text.split()
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
        return [w for w in words if w not in stop_words and len(w) > 2]

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 50:
                chunks.append(chunk)

        return chunks

    def calculate_tf_idf(self):
        """Calculate TF-IDF scores for all chunks"""
        print("📊 Calculating TF-IDF scores...")

        # Calculate document frequency (DF)
        df = defaultdict(int)
        for chunk_data in self.index['chunks']:
            words = set(chunk_data['words'])
            for word in words:
                df[word] += 1

        # Calculate TF-IDF for each chunk
        total_docs = len(self.index['chunks'])
        for i, chunk_data in enumerate(self.index['chunks']):
            word_freq = defaultdict(int)
            for word in chunk_data['words']:
                word_freq[word] += 1

            # Calculate TF-IDF
            tf_idf = {}
            total_words = len(chunk_data['words'])
            for word, freq in word_freq.items():
                tf = freq / total_words if total_words > 0 else 0
                idf = math.log(total_docs / df[word]) if df[word] > 0 else 0
                tf_idf[word] = tf * idf

            chunk_data['tf_idf'] = tf_idf

        print("   ✅ TF-IDF calculation complete")

    def index_study_guides(self):
        """Index all study guide markdown files"""
        print("📚 Indexing study guides...")

        # Find all study guide files
        study_guide_patterns = ["*_GUIDE.md", "*GUIDE.md"]

        # Exclude technical guides
        exclude_keywords = [
            "SETUP", "DEPLOYMENT", "CLOUD", "VISION_MODELING",
            "INTELLIGENCE_BOOST", "COMPLETE_SETUP", "USER_GUIDE",
            "CUSTOM_MODEL", "COLAB", "EASY", "QUICK", "USE_REAL"
        ]

        all_files = []
        for pattern in study_guide_patterns:
            files = glob.glob(os.path.join(self.guides_path, pattern))
            all_files.extend(files)

        # Filter out technical guides
        study_files = [
            f for f in all_files
            if not any(keyword in os.path.basename(f).upper() for keyword in exclude_keywords)
        ]

        # Remove duplicates
        study_files = list(set(study_files))

        print(f"   Found {len(study_files)} study guides")

        # Clear existing index
        self.index = {
            'documents': [],
            'chunks': [],
            'tf_idf': {},
            'doc_count': 0
        }

        total_chunks = 0

        for file_path in study_files:
            filename = os.path.basename(file_path)
            print(f"   📖 Processing: {filename}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract subject from filename
                subject = filename.replace("_GUIDE.md", "").replace("GUIDE.md", "").replace("_", " ").title()

                # Store document info
                doc_id = len(self.index['documents'])
                self.index['documents'].append({
                    'id': doc_id,
                    'filename': filename,
                    'subject': subject,
                    'path': file_path
                })

                # Chunk the content
                chunks = self.chunk_text(content)
                print(f"      Created {len(chunks)} chunks")

                # Process each chunk
                for chunk_idx, chunk in enumerate(chunks):
                    # Preprocess text
                    words = self.preprocess_text(chunk)

                    # Store chunk
                    self.index['chunks'].append({
                        'id': len(self.index['chunks']),
                        'doc_id': doc_id,
                        'chunk_index': chunk_idx,
                        'content': chunk,
                        'words': words,
                        'source': filename,
                        'subject': subject
                    })

                total_chunks += len(chunks)

            except Exception as e:
                print(f"      ❌ Error processing {filename}: {e}")

        self.index['doc_count'] = len(self.index['documents'])

        # Calculate TF-IDF
        if len(self.index['chunks']) > 0:
            self.calculate_tf_idf()

        # Save index
        print(f"\n💾 Saving index to {self.index_path}...")
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
            print("   ✅ Index saved")
        except Exception as e:
            print(f"   ⚠️  Could not save index: {e}")

        print(f"\n✅ Indexing complete!")
        print(f"   Total guides: {len(study_files)}")
        print(f"   Total chunks: {total_chunks}")
        print(f"   Index size: {len(self.index['chunks'])} entries\n")

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two TF-IDF vectors"""
        # Get common words
        common = set(vec1.keys()) & set(vec2.keys())

        if not common:
            return 0.0

        # Calculate dot product
        dot_product = sum(vec1[word] * vec2[word] for word in common)

        # Calculate magnitudes
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant chunks using TF-IDF similarity"""
        if len(self.index['chunks']) == 0:
            return []

        # Preprocess query
        query_words = self.preprocess_text(query)

        # Calculate query TF-IDF
        word_freq = defaultdict(int)
        for word in query_words:
            word_freq[word] += 1

        query_tf_idf = {}
        total_words = len(query_words)
        for word, freq in word_freq.items():
            tf = freq / total_words if total_words > 0 else 0
            # Use existing IDF from index or default to 1
            idf = 1.0
            for chunk_data in self.index['chunks']:
                if word in chunk_data.get('tf_idf', {}):
                    idf = math.log(len(self.index['chunks']))
                    break
            query_tf_idf[word] = tf * idf

        # Calculate similarity with all chunks
        results = []
        for chunk_data in self.index['chunks']:
            chunk_tf_idf = chunk_data.get('tf_idf', {})
            similarity = self.cosine_similarity(query_tf_idf, chunk_tf_idf)

            if similarity > 0:
                results.append({
                    'content': chunk_data['content'],
                    'source': chunk_data['source'],
                    'subject': chunk_data['subject'],
                    'relevance': similarity,
                    'chunk_id': chunk_data['id']
                })

        # Sort by relevance and return top k
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:top_k]

    def get_context_for_question(self, question: str, max_results: int = 3) -> str:
        """Get relevant context from study guides for a question"""
        results = self.search(question, top_k=max_results)

        if not results:
            return ""

        # Build context string
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"## Source {i}: {result['subject']} ({result['source']})\n"
                f"{result['content']}\n"
            )

        return "\n".join(context_parts)

if __name__ == "__main__":
    # Test the simple RAG system
    print("=" * 70)
    print("GENIUS AI - SIMPLE RAG SYSTEM SETUP")
    print("=" * 70)
    print()

    # Initialize
    rag = SimpleRAGSystem()

    # Index study guides
    rag.index_study_guides()

    # Test search
    print("🧪 Testing search functionality...")
    print()

    test_queries = [
        "What is molarity?",
        "Explain photosynthesis",
        "How do you solve quadratic equations?"
    ]

    for query in test_queries:
        print(f"Query: '{query}'")
        results = rag.search(query, top_k=2)

        if results:
            print(f"   Found {len(results)} relevant results:")
            for result in results:
                print(f"   - {result['subject']} (relevance: {result['relevance']:.2f})")
        else:
            print("   No results found")
        print()

    print("=" * 70)
    print("✅ Simple RAG System Ready!")
    print("=" * 70)
