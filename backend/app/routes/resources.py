# backend/app/routes/resources.py
from fastapi import APIRouter
from datetime import datetime
from app.db import get_db

router = APIRouter()
db = get_db()

@router.post("/seed-resources/")
async def seed_resources():
    """
    Insert sample resources into 'Resources' collection.
    Call this once for test data.
    """
    sample_data = [
        {
            "title": "Intro to Probability",
            "topic": "Statistics",
            "url": "https://example.com/probability-intro",
            "difficulty": "beginner",
            "description": "A short video on probability basics",
            "timestamp": datetime.utcnow()
        },
        {
            "title": "Advanced Probability Theories",
            "topic": "Statistics",
            "url": "https://example.com/probability-advanced",
            "difficulty": "advanced",
            "description": "Advanced concepts in probability",
            "timestamp": datetime.utcnow()
        },
        {
            "title": "Basic Algebra Guide",
            "topic": "Algebra",
            "url": "https://example.com/algebra-basic",
            "difficulty": "beginner",
            "description": "Algebra fundamentals",
            "timestamp": datetime.utcnow()
        },
        {
            "title": "Algebra Practice Problems",
            "topic": "Algebra",
            "url": "https://example.com/algebra-practice",
            "difficulty": "intermediate",
            "description": "Exercises for improving algebra skills",
            "timestamp": datetime.utcnow()
        },
        {
            "title": "Khan Academy: Algebra Basics",
            "topic": "Algebra",
            "url": "https://www.khanacademy.org/math/algebra",
            "difficulty": "Beginner",
            "reason": "You got 2 Algebra questions wrong."
        },
        {
            "title": "Geometry Crash Course",
            "topic": "Geometry",
            "url": "https://www.youtube.com/watch?v=Q8lcro0e2sw",
            "difficulty": "Intermediate",
            "reason": "You struggled with geometry angles."
        },
        {
            "title": "Calculus 101",
            "topic": "Calculus",
            "url": "https://example.com/calculus-101",
            "difficulty": "beginner",
            "description": "Introductory calculus course",
            "timestamp": datetime.utcnow()
        }
    ]

    try:
        db.Resources.insert_many(sample_data)
        return {"message": "Sample resources seeded successfully."}
    except Exception as e:
        return {"error": str(e)}

@router.get("/resources/")
async def get_all_resources():
    """Return all resources for debugging."""
    try:
        resources = list(db.Resources.find({}, {"_id": 0}))
        return {"resources": resources}
    except Exception as e:
        return {"error": str(e)}
