# backend/app/models/learning_model.py
from datetime import datetime
from app.db import get_db

db = get_db()

def save_recommendations(user_id: str, recommendations: list) -> None:
    """Save recommendations to 'Recommendations' collection."""
    db.Recommendations.insert_one({
        "user_id": user_id,
        "recommendations": recommendations,
        "timestamp": datetime.utcnow()
    })

def save_quiz_results(user_id: str, quiz_data: dict, score: int) -> None:
    """Save the user's quiz results in 'Quizzes' collection."""
    db.Quizzes.insert_one({
        "user_id": user_id,
        "quiz_data": quiz_data,  # e.g. { questions: [...] }
        "score": score,
        "timestamp": datetime.utcnow()
    })

def update_user_progress(user_id: str, topic: str, progress: int) -> None:
    """
    Update the user's progress in 'Users' collection.
    For a given topic, we store an integer score (0-100).
    """
    db.Users.update_one(
        {"user_id": user_id},
        {"$set": {f"progress.{topic}": progress}},
        upsert=True
    )
