from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_sales_data():
    return {
        "labels": ["January", "February", "March", "April", "May", "June"],
        "data": [300, 400, 200, 500, 700, 600],
    }
