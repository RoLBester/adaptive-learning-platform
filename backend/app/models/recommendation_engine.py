# backend/app/models/recommendation_engine.py
from app.db import get_db

db = get_db()

def recommend_resources_for_user(user_id: str) -> list:
    """
    Naive logic:
    1. Find user doc in Users collection.
    2. Identify topics with progress < 60 => 'weak topics'.
    3. Query 'Resources' for those topics.
    4. Return matched resources or fallback.
    """
    user_doc = db.Users.find_one({"user_id": user_id})
    if not user_doc:
        return ["No user found in the database for user_id: " + user_id]

    progress = user_doc.get("progress", {})
    # e.g. progress = { "Algebra": 40, "Geometry": 75 }

    weak_topics = [topic for topic, score in progress.items() if score < 60]
    if not weak_topics:
        # If no weak topics or user hasn't taken a quiz:
        all_resources = list(db.Resources.find({}, {"_id": 0}))
        return all_resources if all_resources else ["No resources found at all."]

    # Query resources for those topics
    query = {"topic": {"$in": weak_topics}}
    matched_resources = list(db.Resources.find(query, {"_id": 0}))

    if matched_resources:
        return matched_resources
    else:
        return ["No specialized resources found for your weak topics."]
