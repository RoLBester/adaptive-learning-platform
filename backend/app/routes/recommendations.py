# backend/app/routes/recommendations.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.models.recommendation_engine import recommend_resources_for_user
from app.models.learning_model import save_recommendations

router = APIRouter()

class RecommendationRequest(BaseModel):
    user_id: str
    user_data: dict = {}

@router.post("/recommend-content/")
async def recommend_content(request: RecommendationRequest):
    try:
        recommended_items = recommend_resources_for_user(request.user_id)
        # Saves them to "Recommendations" collection (optional)
        save_recommendations(user_id=request.user_id, recommendations=recommended_items)
        return {"user_id": request.user_id, "recommendations": recommended_items}
    except Exception as e:
        return {"error": str(e)}
