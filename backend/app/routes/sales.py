from fastapi import APIRouter
from app.db import db
from datetime import datetime

router = APIRouter()

# Endpoint to save and retrieve sales data
@router.get("/sales/")
async def get_sales_data():
    """Fetch sales data from MongoDB."""
    try:
        sales_data = list(db.Sales.find({}, {"_id": 0}))  # Retrieve sales data
        return {"sales_data": sales_data}
    except Exception as e:
        return {"error": str(e)}

@router.post("/sales/")
async def add_sales_data():
    """Add dummy sales data to MongoDB."""
    try:
        dummy_sales = {
            "labels": ["January", "February", "March", "April", "May", "June"],
            "data": [300, 400, 200, 500, 700, 600],
            "timestamp": datetime.utcnow()
        }
        db.Sales.insert_one(dummy_sales)  # Insert sales data into MongoDB
        return {"message": "Sales data added successfully."}
    except Exception as e:
        return {"error": str(e)}
