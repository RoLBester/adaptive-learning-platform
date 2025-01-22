# backend/app/routes/evaluations.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.models.learning_model import save_quiz_results, update_user_progress

router = APIRouter()

class QuestionData(BaseModel):
    question: str
    topic: str
    userAnswer: str
    correctAnswer: str
    isCorrect: bool

class QuizSubmission(BaseModel):
    user_id: str
    quiz_data: Dict[str, Any]
    score: int
    topic: str

@router.post("/evaluate-quiz/")
async def evaluate_quiz(submission: QuizSubmission):
    """
    Save quiz results + update user progress in 'Users' collection.
    We also handle multiple topics. If each question has a 'topic',
    update progress per topic.
    """
    try:
        # 1) Saves entire quiz results in Quizzes
        save_quiz_results(
            user_id=submission.user_id,
            quiz_data=submission.quiz_data,
            score=submission.score
        )

        # 2) For each question, if the user got it correct => set progress ~100, else <60
        #    
        questions = submission.quiz_data.get("questions", [])
        for q in questions:
            t = q.get("topic", "Unknown")
            is_correct = q.get("isCorrect", False)
            # For simplicity, correct => 80, wrong => 40
            progress_val = 80 if is_correct else 40
            update_user_progress(
                user_id=submission.user_id,
                topic=t,
                progress=progress_val
            )

        return {"message": "Quiz evaluated and progress updated successfully"}
    except Exception as e:
        return {"error": str(e)}
