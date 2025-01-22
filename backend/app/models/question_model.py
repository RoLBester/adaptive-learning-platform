# backend/app/models/question_model.py
from transformers import pipeline
from app.db import get_db

db = get_db()

# This uses a pre-trained Hugging Face QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(question: str, context: str) -> str:
    try:
        response = qa_pipeline(question=question, context=context)
        return response.get("answer", "No answer found")
    except Exception as e:
        print(f"Error during QA pipeline: {e}")
        return "Error generating an answer."

def save_question_answer(question: str, context: str, answer: str) -> None:
    db.Questions.insert_one({
        "question": question,
        "context": context,
        "answer": answer
    })
