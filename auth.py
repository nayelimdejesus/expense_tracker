import os
from pymongo import MongoClient
from dotenv import load_dotenv
from db import db

users_collection = db["users"]

#register user
def register_user():
    while True:
        print("\n*** Register New Account ***")
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        #if user exist print error and try different username
        user_found = users_collection.find_one({"username":username})
 
        if user_found == None:
            users_collection.insert_one({
                "username": username,
                "password": password,  
                "expenses": []       
            })
            print("\nRegistered successfully!\n")
            return True
        else:
            print("\n*** User Exists. Please try again. ***\n")

def login(username, password):
    user_exist = users_collection.find_one({"username":username})
    if user_exist and user_exist["password"] == password:
        print(f"Welcome back! {username}")
    return False


# register_user()
