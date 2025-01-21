from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from importlib import import_module
from app.cors import add_cors_middleware  # Import the CORS configuration

import os

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Dynamically import and include the sales router
try:
    sales_router = import_module("app.routes.sales").router
    app.include_router(sales_router, prefix="/api/sales", tags=["sales"])
except ModuleNotFoundError as e:
    print(f"Error importing sales module: {e}")

# Load environment variables
load_dotenv()
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
try:
    client = MongoClient(uri)
    db = client["AdaptiveLearning"]
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None  # Ensure `db` is defined even if the connection fails

# Test MongoDB connection and return a message
@app.get("/")
async def root():
    if db is None:
        return {"error": "MongoDB connection is not established"}

    try:
        collections = db.list_collection_names()
        return {
            "message": "Hello, Adaptive Learning Platform is running!",
            "collections": collections,
        }
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}