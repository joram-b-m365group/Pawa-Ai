"""Vector store implementation using ChromaDB."""

from typing import Any
from uuid import uuid4

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from genius_ai.core.config import settings
from genius_ai.core.logger import logger


class VectorStore:
    """Vector database for storing and retrieving knowledge."""

    def __init__(
        self,
        collection_name: str | None = None,
        embedding_model: str | None = None,
    ):
        """Initialize vector store.

        Args:
            collection_name: Name of the collection
            embedding_model: Name of embedding model to use
        """
        self.collection_name = collection_name or settings.chroma_collection_name
        self.embedding_model_name = embedding_model or settings.embedding_model

        self._client = None
        self._collection = None
        self._embedding_model = None

    async def initialize(self) -> None:
        """Initialize ChromaDB client and collection."""
        logger.info("Initializing vector store")

        # Initialize ChromaDB
        self._client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Genius AI knowledge base"},
        )

        # Load embedding model
        logger.info(f"Loading embedding model: {self.embedding_model_name}")
        self._embedding_model = SentenceTransformer(self.embedding_model_name)

        logger.info("Vector store initialized")

    def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        if self._embedding_model is None:
            raise RuntimeError("Embedding model not initialized")

        embedding = self._embedding_model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding.tolist()

    async def add_documents(
        self,
        documents: list[str],
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
    ) -> list[str]:
        """Add documents to vector store.

        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents

        Returns:
            List of document IDs
        """
        if self._collection is None:
            await self.initialize()

        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid4()) for _ in documents]

        # Generate embeddings
        logger.info(f"Adding {len(documents)} documents to vector store")
        embeddings = [self._generate_embedding(doc) for doc in documents]

        # Add to collection
        self._collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

        logger.info(f"Added {len(documents)} documents")
        return ids

    async def search(
        self,
        query: str,
        top_k: int | None = None,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of search results with documents and metadata
        """
        if self._collection is None:
            await self.initialize()

        top_k = top_k or settings.top_k_results

        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        # Search
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
                "id": results["ids"][0][i] if results["ids"] else None,
            })

        return formatted_results

    async def delete_documents(self, ids: list[str]) -> None:
        """Delete documents by IDs.

        Args:
            ids: List of document IDs to delete
        """
        if self._collection is None:
            await self.initialize()

        self._collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents")

    async def clear(self) -> None:
        """Clear all documents from collection."""
        if self._collection is None:
            await self.initialize()

        self._collection.delete()
        logger.info("Cleared vector store")

    def count(self) -> int:
        """Get count of documents in collection.

        Returns:
            Number of documents
        """
        if self._collection is None:
            return 0

        return self._collection.count()
