"""
Vector Store Module - ChromaDB Integration for RAG

Manages the vector database for semantic search of educational resources.
Uses ChromaDB for persistent local storage and sentence-transformers for generating embeddings.

Implementation details:
- VectorStore class provides the main interface for all vector operations
- Embeddings generated using sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- Semantic search powered by cosine similarity
- Data persisted to disk in backend/chroma_db/
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os
from pathlib import Path


class VectorStore:
    """
    Manages vector embeddings and semantic search for educational resources.

    This class provides a simple interface to:
    1. Store resource embeddings in ChromaDB
    2. Perform semantic similarity search
    3. Persist data to disk for reuse
    """

    def __init__(self, persist_directory: str = None):
        """
        Initialize the vector store with ChromaDB and embedding model.

        Args:
            persist_directory: Path to store ChromaDB data (default: backend/chroma_db)
        """
        # Set up persistence directory
        if persist_directory is None:
            backend_dir = Path(__file__).parent.parent.parent
            persist_directory = str(backend_dir / "chroma_db")

        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        print(f"[VectorStore] Initializing ChromaDB at: {persist_directory}")

        # Initialize ChromaDB client with persistence
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))

        # Get or create collection for educational resources
        self.collection = self.client.get_or_create_collection(
            name="educational_resources",
            metadata={"description": "Study materials for adaptive learning"}
        )

        # Load sentence transformer model for embeddings
        # all-MiniLM-L6-v2: Fast, small (80MB), good quality (384 dimensions)
        print("[VectorStore] Loading embedding model: all-MiniLM-L6-v2")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        print(f"[VectorStore] Initialized successfully. Collection size: {self.collection.count()}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a text string.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the 384-dimensional embedding
        """
        embedding = self.embedding_model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def add_resource(
        self,
        resource_id: str,
        title: str,
        description: str,
        topic: str,
        metadata: Dict[str, Any]
    ):
        """
        Add a single resource to the vector store.

        Args:
            resource_id: Unique identifier for the resource
            title: Resource title
            description: Resource description
            topic: Subject topic (e.g., "Algebra", "Calculus")
            metadata: Additional metadata (url, difficulty, etc.)
        """
        # Combine title, description, and topic for rich semantic representation
        combined_text = f"{title}. {description}. Topic: {topic}"

        # Generate embedding
        embedding = self.generate_embedding(combined_text)

        # Store in ChromaDB
        self.collection.add(
            ids=[resource_id],
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[{
                "title": title,
                "description": description,
                "topic": topic,
                **metadata
            }]
        )

    def add_resources_batch(self, resources: List[Dict[str, Any]]):
        """
        Add multiple resources to the vector store in batch.

        Args:
            resources: List of resource dictionaries with keys:
                      - id, title, description, topic, and other metadata
        """
        if not resources:
            print("[VectorStore] No resources to add")
            return

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        print(f"[VectorStore] Embedding {len(resources)} resources...")

        for resource in resources:
            # Generate unique ID if not provided
            resource_id = resource.get("id") or resource.get("title", "").replace(" ", "_")

            title = resource.get("title", "")
            description = resource.get("description", "")
            topic = resource.get("topic", "")

            # Combine for embedding
            combined_text = f"{title}. {description}. Topic: {topic}"

            # Generate embedding
            embedding = self.generate_embedding(combined_text)

            # Prepare metadata (exclude _id from MongoDB if present)
            metadata = {k: v for k, v in resource.items() if k != "_id"}
            metadata.update({
                "title": title,
                "description": description,
                "topic": topic
            })

            ids.append(resource_id)
            embeddings.append(embedding)
            documents.append(combined_text)
            metadatas.append(metadata)

        # Batch insert
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        print(f"[VectorStore] Successfully added {len(resources)} resources")

    def semantic_search(
        self,
        query: str,
        n_results: int = 5,
        min_similarity: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search to find relevant resources.

        Args:
            query: Search query (e.g., "algebra basics for beginners")
            n_results: Number of results to return (default: 5)
            min_similarity: Minimum similarity threshold 0-1 (default: 0.5)

        Returns:
            List of dictionaries containing:
            - metadata: Resource information
            - similarity: Similarity score (0-1, higher is better)
            - document: Original text that was embedded
        """
        if self.collection.count() == 0:
            print("[VectorStore] No resources in database")
            return []

        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        formatted_results = []

        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                # ChromaDB returns distances, convert to similarity (1 - distance)
                # For cosine similarity: similarity = 1 - distance
                distance = results['distances'][0][i] if results['distances'] else 0
                similarity = 1 - distance

                # Filter by minimum similarity
                if similarity >= min_similarity:
                    formatted_results.append({
                        "metadata": results['metadatas'][0][i],
                        "similarity": round(similarity, 3),
                        "document": results['documents'][0][i],
                        "id": results['ids'][0][i]
                    })

        print(f"[VectorStore] Found {len(formatted_results)} results for query: '{query}'")
        return formatted_results

    def clear_collection(self):
        """
        Clear all data from the collection (use for testing/debugging).
        """
        self.client.delete_collection("educational_resources")
        self.collection = self.client.get_or_create_collection(
            name="educational_resources",
            metadata={"description": "Study materials for adaptive learning"}
        )
        print("[VectorStore] Collection cleared")

    def get_collection_size(self) -> int:
        """
        Get the number of resources in the vector store.

        Returns:
            Number of stored resources
        """
        return self.collection.count()


# Global instance (singleton pattern)
_vector_store_instance = None


def get_vector_store() -> VectorStore:
    """
    Get or create the global VectorStore instance.

    Returns:
        VectorStore instance
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance
