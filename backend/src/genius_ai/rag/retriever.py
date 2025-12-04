"""Document retrieval and chunking for RAG."""

import re
from dataclasses import dataclass
from typing import Any

from genius_ai.core.config import settings
from genius_ai.core.logger import logger
from genius_ai.rag.vector_store import VectorStore


@dataclass
class Document:
    """Represents a document chunk."""

    content: str
    metadata: dict[str, Any]
    id: str | None = None


class DocumentChunker:
    """Splits documents into chunks for embedding."""

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        """Initialize chunker.

        Args:
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    def chunk_text(self, text: str, metadata: dict[str, Any] | None = None) -> list[Document]:
        """Split text into chunks.

        Args:
            text: Text to chunk
            metadata: Metadata to attach to chunks

        Returns:
            List of document chunks
        """
        metadata = metadata or {}

        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph fits in current chunk
            if len(current_chunk) + len(para) + 1 <= self.chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
            else:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append(Document(
                        content=current_chunk,
                        metadata=metadata.copy(),
                    ))

                # If paragraph itself is too large, split it
                if len(para) > self.chunk_size:
                    sub_chunks = self._split_large_text(para)
                    chunks.extend([
                        Document(content=chunk, metadata=metadata.copy())
                        for chunk in sub_chunks
                    ])
                    current_chunk = ""
                else:
                    current_chunk = para

        # Add final chunk
        if current_chunk:
            chunks.append(Document(
                content=current_chunk,
                metadata=metadata.copy(),
            ))

        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks

    def _split_large_text(self, text: str) -> list[str]:
        """Split large text by sentences.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                # If single sentence is too large, split by words
                if len(sentence) > self.chunk_size:
                    words = sentence.split()
                    temp_chunk = ""
                    for word in words:
                        if len(temp_chunk) + len(word) + 1 <= self.chunk_size:
                            if temp_chunk:
                                temp_chunk += " " + word
                            else:
                                temp_chunk = word
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk)
                            temp_chunk = word
                    current_chunk = temp_chunk
                else:
                    current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks


class RAGRetriever:
    """Retrieval-Augmented Generation system."""

    def __init__(self, vector_store: VectorStore | None = None):
        """Initialize RAG retriever.

        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store or VectorStore()
        self.chunker = DocumentChunker()

    async def initialize(self) -> None:
        """Initialize retriever."""
        await self.vector_store.initialize()

    async def add_documents(
        self,
        documents: list[str] | list[Document],
        chunk: bool = True,
    ) -> int:
        """Add documents to knowledge base.

        Args:
            documents: List of documents to add
            chunk: Whether to chunk documents

        Returns:
            Number of chunks added
        """
        all_chunks = []

        for doc in documents:
            if isinstance(doc, str):
                # Convert string to Document
                doc = Document(content=doc, metadata={})

            if chunk:
                # Chunk the document
                chunks = self.chunker.chunk_text(doc.content, doc.metadata)
                all_chunks.extend(chunks)
            else:
                all_chunks.append(doc)

        # Add to vector store
        await self.vector_store.add_documents(
            documents=[chunk.content for chunk in all_chunks],
            metadatas=[chunk.metadata for chunk in all_chunks],
        )

        logger.info(f"Added {len(all_chunks)} document chunks to knowledge base")
        return len(all_chunks)

    async def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant documents for query.

        Args:
            query: Search query
            top_k: Number of results
            filter_metadata: Metadata filters

        Returns:
            List of relevant documents
        """
        results = await self.vector_store.search(
            query=query,
            top_k=top_k,
            filter_metadata=filter_metadata,
        )

        logger.info(f"Retrieved {len(results)} documents for query")
        return results

    async def retrieve_context(
        self,
        query: str,
        top_k: int | None = None,
        separator: str = "\n\n---\n\n",
    ) -> str:
        """Retrieve and format context for prompt.

        Args:
            query: Search query
            top_k: Number of results
            separator: Separator between documents

        Returns:
            Formatted context string
        """
        results = await self.retrieve(query, top_k)

        if not results:
            return ""

        context_parts = []
        for i, result in enumerate(results, 1):
            doc = result["document"]
            context_parts.append(f"[Document {i}]\n{doc}")

        context = separator.join(context_parts)
        logger.info(f"Generated context with {len(results)} documents")

        return context
