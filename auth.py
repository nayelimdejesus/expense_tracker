import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from db import db
from colorama import Fore, Back, Style, init

users_collection = db["users"]
init(autoreset=True)



#register user
def register_user():
    while True:
        print("\n*** Register New Account ***")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not valid_email:
             print(Fore.RED+f"\nInvalid email. Please try again.")
             continue
        
        user_found = users_collection.find_one({"username":username})
        email_found = users_collection.find_one({"email":email})

        if user_found == None and email_found == None:
            pwd_byte = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(pwd_byte, salt)
            users_collection.insert_one({
                "username": username,
                "password": hash_password,  
                "expenses": []       
            })
            print(Fore.GREEN+f"\nRegistered successfully!")
            return True
        else:
            print("\n*** User Exists. Please try again. ***\n")

def login():
    while True:
        print("\n*** Login ***")
        username = input("Enter username: ")
        pwd = input("Enter password: ")
        user_exist = users_collection.find_one({"username":username})
        if user_exist:
            user_byte = pwd.encode('utf-8')
            stored_pwd = user_exist['password']
            result = bcrypt.checkpw(user_byte, stored_pwd)
            if result and pwd != "":
                print(Fore.GREEN+f"\nWelcome back! {username}")
                return True
        else:
            print(Fore.RED+"\nInvalid credentials. Please try again.")
            