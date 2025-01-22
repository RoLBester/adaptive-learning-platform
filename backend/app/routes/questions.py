# backend/app/routes/questions.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.models.question_model import answer_question, save_question_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    context: str

@router.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    try:
        ans = answer_question(request.question, request.context)
        save_question_answer(request.question, request.context, ans)
        return {"question": request.question, "answer": ans}
    except Exception as e:
        return {"error": str(e)}
