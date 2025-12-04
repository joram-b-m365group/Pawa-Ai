"""
RAG (Retrieval-Augmented Generation) System for Genius AI
Indexes and searches through all study guides
"""
import os
import sys
import glob
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

class RAGSystem:
    def __init__(self, guides_path: str = "../", db_path: str = "./chroma_db"):
        """Initialize RAG system with ChromaDB and embeddings model"""
        print("🔧 Initializing RAG System...")

        # Initialize embedding model (lightweight, runs locally)
        print("   Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✅ Embedding model loaded")

        # Initialize ChromaDB
        print("   Setting up vector database...")
        self.client = chromadb.PersistentClient(path=db_path)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="study_guides",
            metadata={"description": "All Genius AI study guides"}
        )
        print("   ✅ Vector database ready")

        self.guides_path = guides_path
        print("✅ RAG System initialized!\n")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better retrieval"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 50:  # Skip very small chunks
                chunks.append(chunk)

        return chunks

    def index_study_guides(self):
        """Index all study guide markdown files"""
        print("📚 Indexing study guides...")

        # Find all study guide files (excluding technical docs)
        study_guide_patterns = [
            "*_GUIDE.md",
            "*GUIDE.md"
        ]

        # Educational guides only (exclude technical setup guides)
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

        print(f"   Found {len(study_files)} study guides")

        # Check if already indexed
        existing_count = self.collection.count()
        if existing_count > 0:
            print(f"   ⚠️  Database already has {existing_count} chunks")
            response = input("   Re-index? (y/n): ").lower()
            if response != 'y':
                print("   Skipping indexing")
                return
            # Clear existing data
            self.collection.delete(where={})
            print("   Cleared existing data")

        total_chunks = 0

        for file_path in study_files:
            filename = os.path.basename(file_path)
            print(f"   📖 Processing: {filename}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract subject from filename
                subject = filename.replace("_GUIDE.md", "").replace("GUIDE.md", "").replace("_", " ").title()

                # Chunk the content
                chunks = self.chunk_text(content)
                print(f"      Created {len(chunks)} chunks")

                # Add to ChromaDB
                ids = [f"{filename}_{i}" for i in range(len(chunks))]
                metadatas = [
                    {
                        "source": filename,
                        "subject": subject,
                        "chunk_index": i
                    }
                    for i in range(len(chunks))
                ]

                self.collection.add(
                    documents=chunks,
                    ids=ids,
                    metadatas=metadatas
                )

                total_chunks += len(chunks)

            except Exception as e:
                print(f"      ❌ Error processing {filename}: {e}")

        print(f"\n✅ Indexing complete!")
        print(f"   Total guides: {len(study_files)}")
        print(f"   Total chunks: {total_chunks}")
        print(f"   Database size: {self.collection.count()} entries\n")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant content in study guides"""
        try:
            # Query the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )

            # Format results
            formatted_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'source': results['metadatas'][0][i]['source'],
                        'subject': results['metadatas'][0][i]['subject'],
                        'relevance': 1.0 - results['distances'][0][i] if 'distances' in results else 1.0
                    })

            return formatted_results

        except Exception as e:
            print(f"Search error: {e}")
            return []

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
    # Test the RAG system
    print("=" * 70)
    print("GENIUS AI - RAG SYSTEM SETUP")
    print("=" * 70)
    print()

    # Initialize
    rag = RAGSystem()

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
    print("✅ RAG System Ready!")
    print("=" * 70)
