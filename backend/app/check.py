
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Diddy:Z5DfPphyo0HSWJk3@cluster0.y3ojh.mongodb.net/AdaptiveLearning?retryWrites=true&w=majority"

# Creates a new client and connects to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Sends a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)