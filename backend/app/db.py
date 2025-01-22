from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Loads environment variables
load_dotenv()
uri = os.getenv("MONGO_URI")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# MongoDB Connection
client = MongoClient(uri)
db = client["AdaptiveLearning"]

def get_db():
    """Return the database instance."""
    return db
