import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from colorama import Fore, Back, Style, init



load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where()) 
    client.server_info() 
    db = client["Users"]
    print("Connected to MongoDB successfully!\n")
except Exception as e:
    print("Connection failed:\n", e)
