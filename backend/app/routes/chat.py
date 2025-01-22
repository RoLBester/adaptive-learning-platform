# app/routes/chat.py

import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

router = APIRouter()

class ChatRequest(BaseModel):
    conversation: List[str]
    # e.g. ["Hello", "Hi! Who are you?", "I want help with integrals..."]

@router.post("/chat/")
async def chat_with_model(request: ChatRequest):
    """
    Calls the Hugging Face Inference API for 'meta-llama/Llama-2-7b-hf'.
    """
    if not HUGGINGFACE_TOKEN:
        return {"error": "No HUGGINGFACE_TOKEN found in environment."}

    # Combines conversation into a single 'prompt'
    # For example, labels user + AI turns OR just plain text
    # Adds an instruction: "You are a helpful tutor..."
    prompt_text = "You are a helpful tutor.\n\nConversation:\n"
    for i, msg in enumerate(request.conversation):
        prompt_text += f"{msg}\n"
    prompt_text += "\nAnswer the user clearly:\n"

    # Uses Llama-2-7b-hf
    HF_MODEL_ID = "meta-llama/Llama-2-7b-hf"

    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": prompt_text,
        "parameters": {
            # You can tweak generation params
            "max_new_tokens": 150,
            "temperature": 0.7,
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            bot_reply = data[0]["generated_text"]
        else:
            bot_reply = "No coherent reply. Check model response."

        return {"reply": bot_reply}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
