# backend/app/routes/performance.py
from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.get("/user-performance/{user_id}")
async def get_user_performance(user_id: str):
    """
    Return an array of all questions from all quizzes the user has taken,
    along with whether they were correct or not, for the bar chart.
    """
    db = get_db()
    quizzes = db.Quizzes.find({"user_id": user_id}, {"_id": 0})

    performance_data = []
    index_counter = 1

    for quiz in quizzes:
        q_data = quiz.get("quiz_data", {}).get("questions", [])
        for q in q_data:
            is_correct = q.get("isCorrect", False)
            question_text = q.get("question", "")
            performance_data.append({
                "index": index_counter,
                "question": question_text,
                "isCorrect": is_correct
            })
            index_counter += 1

    return {"performance": performance_data}
