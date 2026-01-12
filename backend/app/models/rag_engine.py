"""
RAG Engine - Retrieval-Augmented Generation for Personalized Recommendations

Implements intelligent recommendation logic by combining user performance analysis
with semantic search to deliver context-aware study material suggestions.

Features:
- Analyzes quiz performance to identify weak areas
- Generates semantic queries based on specific learning gaps
- Performs vector search to find relevant study materials
- Ranks results by relevance score and difficulty level
"""

from typing import List, Dict, Any
from app.db import get_db
from app.models.vector_store import get_vector_store


class RAGRecommendationEngine:
    """
    Intelligent recommendation engine using RAG principles.

    This engine goes beyond simple keyword matching by:
    1. Understanding the semantic context of user's weak areas
    2. Generating intelligent search queries
    3. Finding semantically similar resources
    4. Ranking by relevance and user level
    """

    def __init__(self):
        self.db = get_db()
        self.vector_store = get_vector_store()

    def analyze_user_performance(self, user_id: str) -> Dict[str, Any]:
        """
        Analyze user's quiz performance to identify learning gaps.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with:
            - weak_topics: List of topics where user scored < 60%
            - strong_topics: List of topics where user scored >= 60%
            - overall_score: Average score across all topics
            - has_data: Whether user has taken any quizzes
        """
        user_doc = self.db.Users.find_one({"user_id": user_id})

        if not user_doc:
            return {
                "weak_topics": [],
                "strong_topics": [],
                "overall_score": 0,
                "has_data": False
            }

        progress = user_doc.get("progress", {})

        if not progress:
            return {
                "weak_topics": [],
                "strong_topics": [],
                "overall_score": 0,
                "has_data": False
            }

        weak_topics = [topic for topic, score in progress.items() if score < 60]
        strong_topics = [topic for topic, score in progress.items() if score >= 60]
        overall_score = sum(progress.values()) / len(progress) if progress else 0

        return {
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "overall_score": round(overall_score, 2),
            "has_data": True
        }

    def generate_search_query(self, weak_topics: List[str], user_level: str = "beginner") -> str:
        """
        Generate an intelligent search query based on weak topics.

        Args:
            weak_topics: List of topics where user is struggling
            user_level: User's proficiency level (beginner/intermediate/advanced)

        Returns:
            Semantic search query string
        """
        if not weak_topics:
            return f"{user_level} mathematics study materials"

        # Create a rich semantic query
        topics_str = " ".join(weak_topics)
        query = f"{user_level} {topics_str} fundamentals basics introduction tutorial"

        return query

    def rag_recommend(
        self,
        user_id: str,
        n_results: int = 5,
        min_similarity: float = 0.5
    ) -> Dict[str, Any]:
        """
        Generate RAG-based recommendations for a user.

        This is the main recommendation function that:
        1. Analyzes user performance
        2. Generates semantic queries
        3. Performs vector search
        4. Returns ranked, relevant resources

        Args:
            user_id: User identifier
            n_results: Maximum number of recommendations (default: 5)
            min_similarity: Minimum similarity threshold 0-1 (default: 0.5)

        Returns:
            Dictionary containing:
            - user_id: User identifier
            - analysis: Performance analysis
            - recommendations: List of recommended resources with similarity scores
            - query_used: The semantic query that was used
            - method: "rag" to indicate RAG-based recommendations
        """
        # Step 1: Analyze user performance
        analysis = self.analyze_user_performance(user_id)

        # Step 2: Handle case where user has no data
        if not analysis["has_data"]:
            # Return general beginner resources using semantic search
            query = "beginner mathematics fundamentals introduction basics"
            results = self.vector_store.semantic_search(
                query=query,
                n_results=n_results,
                min_similarity=0.3  # Lower threshold for general recommendations
            )

            return {
                "user_id": user_id,
                "analysis": analysis,
                "recommendations": [self._format_recommendation(r) for r in results],
                "query_used": query,
                "method": "rag",
                "message": "No quiz data found. Showing general beginner resources."
            }

        # Step 3: Generate semantic query based on weak topics
        weak_topics = analysis["weak_topics"]

        if not weak_topics:
            # User is doing well on all topics
            return {
                "user_id": user_id,
                "analysis": analysis,
                "recommendations": [],
                "query_used": None,
                "method": "rag",
                "message": "Great job! No weak areas detected. Keep up the good work!"
            }

        # Determine user level based on overall score
        overall_score = analysis["overall_score"]
        if overall_score < 40:
            user_level = "beginner"
        elif overall_score < 70:
            user_level = "intermediate"
        else:
            user_level = "advanced"

        query = self.generate_search_query(weak_topics, user_level)

        # Step 4: Perform semantic search
        results = self.vector_store.semantic_search(
            query=query,
            n_results=n_results,
            min_similarity=min_similarity
        )

        # Step 5: Format and return recommendations
        recommendations = [self._format_recommendation(r) for r in results]

        return {
            "user_id": user_id,
            "analysis": analysis,
            "recommendations": recommendations,
            "query_used": query,
            "method": "rag",
            "message": f"Found {len(recommendations)} personalized resources for your weak areas."
        }

    def _format_recommendation(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a vector search result into a recommendation.

        Args:
            result: Raw result from vector store

        Returns:
            Formatted recommendation dictionary
        """
        metadata = result["metadata"]

        return {
            "title": metadata.get("title", ""),
            "topic": metadata.get("topic", ""),
            "url": metadata.get("url", ""),
            "difficulty": metadata.get("difficulty", "beginner"),
            "description": metadata.get("description", ""),
            "similarity_score": result["similarity"],
            "relevance": self._get_relevance_label(result["similarity"])
        }

    def _get_relevance_label(self, similarity: float) -> str:
        """
        Convert similarity score to human-readable relevance label.

        Args:
            similarity: Similarity score (0-1)

        Returns:
            Relevance label (Highly Relevant/Relevant/Somewhat Relevant)
        """
        if similarity >= 0.8:
            return "Highly Relevant"
        elif similarity >= 0.6:
            return "Relevant"
        else:
            return "Somewhat Relevant"

    def compare_with_baseline(self, user_id: str) -> Dict[str, Any]:
        """
        Compare RAG recommendations with baseline keyword matching.

        This is useful for demonstrating the improvement of RAG over simple matching.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with both RAG and baseline recommendations
        """
        # Get RAG recommendations
        rag_results = self.rag_recommend(user_id)

        # Get baseline recommendations (simple topic matching)
        from app.models.recommendation_engine import recommend_resources_for_user
        baseline_results = recommend_resources_for_user(user_id)

        return {
            "user_id": user_id,
            "rag_recommendations": rag_results,
            "baseline_recommendations": baseline_results,
            "comparison": {
                "rag_count": len(rag_results.get("recommendations", [])),
                "baseline_count": len(baseline_results) if isinstance(baseline_results, list) else 0,
                "rag_personalized": rag_results.get("analysis", {}).get("has_data", False)
            }
        }


# Global instance
_rag_engine_instance = None


def get_rag_engine() -> RAGRecommendationEngine:
    """
    Get or create the global RAGRecommendationEngine instance.

    Returns:
        RAGRecommendationEngine instance
    """
    global _rag_engine_instance
    if _rag_engine_instance is None:
        _rag_engine_instance = RAGRecommendationEngine()
    return _rag_engine_instance
