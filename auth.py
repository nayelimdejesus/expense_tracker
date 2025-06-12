import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from db import db
from colorama import Fore, Back, Style, init
import getpass

users_collection = db["users"]
init(autoreset=True)

def register_user():
    #prompts user to enter registration information
    count = 0
    while count <= 3:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+"\nRegister New Account")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        #checks if email is valid
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not valid_email:
             print(Fore.RED+f"\nInvalid email. Please try again.")
             continue
        
        #checks if email or username do not exist -> create account
        user_found = users_collection.find_one({"username":username})
        email_found = users_collection.find_one({"email":email})

        if user_found == None and email_found == None:
            pwd_byte = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(pwd_byte, salt)
            users_collection.insert_one({
                "username": username,
                "email":email,
                "password": hash_password
            })
            print(Fore.GREEN+f"\nRegistered successfully! Returning to Main Menu ...")
            return username
        
        count += 1
        if count == 3:
            print(Fore.RED + Style.BRIGHT + "\nToo many failed attempts. Returning to Main Menu ...")
            return
        else: 
            print(Fore.RED + "\n*** User Exists. Please try again. ***\n")
            

def login():
    #prompts user to enter login information
    count = 0
    while count <= 3:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+"\nLogin To Your Account")
        username = input("Enter username: ")
        pwd = getpass.getpass("Enter password: ")
        
        #if user exist it checks if password matches the password in the database
        user_exist = users_collection.find_one({"username":username})
        if user_exist:
            user_byte = pwd.encode('utf-8')
            stored_pwd = user_exist['password']
            result = bcrypt.checkpw(user_byte, stored_pwd)
            if result and pwd != "":
                print(Fore.GREEN+f"\nLogged in as {username}")
                return username
        
        count += 1
        if count == 3:
            print(Fore.RED + Style.BRIGHT + "\nToo many failed attempts. Returning to Main Menu ...")
            return 
        else:
            print(Fore.RED + "\nInvalid credentials. Please try again.")
            

            
            