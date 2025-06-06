import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI) 
    client.server_info() 
    print("Connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)

