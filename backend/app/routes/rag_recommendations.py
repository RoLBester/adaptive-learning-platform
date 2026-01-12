"""
RAG Recommendations API Routes

Implements RESTful endpoints for the RAG-enhanced recommendation system.
Handles semantic search queries, vector database management, and performance comparisons.

Endpoints:
- POST /api/rag-recommend/ - Get personalized RAG recommendations
- POST /api/embed-resources/ - Embed resources into vector database
- GET /api/vector-stats/ - Get vector database statistics
- POST /api/compare-recommendations/ - Compare RAG vs baseline
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.rag_engine import get_rag_engine
from app.models.vector_store import get_vector_store
from app.db import get_db

router = APIRouter()


class RAGRecommendationRequest(BaseModel):
    """Request model for RAG recommendations."""
    user_id: str
    n_results: Optional[int] = 5
    min_similarity: Optional[float] = 0.5


class EmbedResourcesRequest(BaseModel):
    """Request model for embedding resources."""
    clear_existing: Optional[bool] = False


@router.post("/rag-recommend/")
async def rag_recommend(request: RAGRecommendationRequest):
    """
    Get personalized RAG-based recommendations for a user.

    This endpoint:
    1. Analyzes the user's quiz performance
    2. Identifies weak topics
    3. Performs semantic search for relevant resources
    4. Returns ranked recommendations with similarity scores

    Request Body:
    - user_id: User identifier (e.g., "user123")
    - n_results: Maximum number of recommendations (default: 5)
    - min_similarity: Minimum similarity threshold 0-1 (default: 0.5)

    Response:
    - user_id: User identifier
    - analysis: Performance breakdown (weak_topics, overall_score, etc.)
    - recommendations: List of resources with similarity scores
    - query_used: The semantic query that was generated
    - method: "rag"
    - message: Human-readable status message

    Example:
    ```
    POST /api/rag-recommend/
    {
        "user_id": "user123",
        "n_results": 5,
        "min_similarity": 0.6
    }
    ```
    """
    try:
        rag_engine = get_rag_engine()

        result = rag_engine.rag_recommend(
            user_id=request.user_id,
            n_results=request.n_results,
            min_similarity=request.min_similarity
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG recommendation failed: {str(e)}")


@router.post("/embed-resources/")
async def embed_resources(request: EmbedResourcesRequest):
    """
    Embed all resources from MongoDB into the vector database.

    This is a one-time setup endpoint (or run after adding new resources).
    It reads all resources from the MongoDB Resources collection,
    generates embeddings, and stores them in ChromaDB.

    Request Body:
    - clear_existing: If true, clears existing embeddings before adding new ones (default: false)

    Response:
    - message: Success message
    - resources_embedded: Number of resources processed
    - collection_size: Total size of vector database after operation

    Example:
    ```
    POST /api/embed-resources/
    {
        "clear_existing": false
    }
    ```

    Note: This operation can take 30-60 seconds for 50-100 resources
    """
    try:
        vector_store = get_vector_store()
        db = get_db()

        # Optionally clear existing data
        if request.clear_existing:
            vector_store.clear_collection()
            print("[API] Cleared existing vector embeddings")

        # Fetch all resources from MongoDB
        resources = list(db.Resources.find({}))

        if not resources:
            return {
                "message": "No resources found in database. Please seed resources first.",
                "resources_embedded": 0,
                "collection_size": 0
            }

        # Convert MongoDB documents to the format expected by vector store
        formatted_resources = []
        for idx, resource in enumerate(resources):
            formatted_resource = {
                "id": f"resource_{idx}",
                "title": resource.get("title", ""),
                "description": resource.get("description", resource.get("reason", "")),
                "topic": resource.get("topic", ""),
                "url": resource.get("url", ""),
                "difficulty": resource.get("difficulty", "beginner")
            }
            formatted_resources.append(formatted_resource)

        # Embed resources in batch
        vector_store.add_resources_batch(formatted_resources)

        collection_size = vector_store.get_collection_size()

        return {
            "message": f"Successfully embedded {len(formatted_resources)} resources",
            "resources_embedded": len(formatted_resources),
            "collection_size": collection_size
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")


@router.get("/vector-stats/")
async def get_vector_stats():
    """
    Get statistics about the vector database.

    Returns:
    - collection_size: Number of resources in vector database
    - embedding_model: Name of the embedding model used
    - embedding_dimension: Dimension of embedding vectors
    - status: "ready" if database has resources, "empty" otherwise

    Example:
    ```
    GET /api/vector-stats/
    ```
    """
    try:
        vector_store = get_vector_store()
        collection_size = vector_store.get_collection_size()

        return {
            "collection_size": collection_size,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimension": 384,
            "status": "ready" if collection_size > 0 else "empty",
            "message": f"Vector database contains {collection_size} embedded resources"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/compare-recommendations/")
async def compare_recommendations(request: RAGRecommendationRequest):
    """
    Compare RAG recommendations with baseline keyword matching.

    This endpoint is useful for demonstrating the improvement of RAG
    over simple topic-based matching.

    Request Body:
    - user_id: User identifier

    Response:
    - user_id: User identifier
    - rag_recommendations: Results from RAG system
    - baseline_recommendations: Results from old keyword system
    - comparison: Side-by-side comparison metrics

    Example:
    ```
    POST /api/compare-recommendations/
    {
        "user_id": "user123"
    }
    ```
    """
    try:
        rag_engine = get_rag_engine()

        comparison = rag_engine.compare_with_baseline(request.user_id)

        return comparison

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.post("/semantic-search/")
async def semantic_search(query: str, n_results: int = 5):
    """
    Perform raw semantic search (for testing/debugging).

    Query Parameters:
    - query: Search query string
    - n_results: Number of results to return (default: 5)

    Response:
    - query: The search query used
    - results: List of matching resources with similarity scores

    Example:
    ```
    POST /api/semantic-search/?query=algebra basics&n_results=3
    ```
    """
    try:
        vector_store = get_vector_store()

        results = vector_store.semantic_search(
            query=query,
            n_results=n_results,
            min_similarity=0.3
        )

        return {
            "query": query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
