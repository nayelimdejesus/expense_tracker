import os
from auth import register_user, login

def main():
    print("Welcome to the Expense App\n")
    print("Make a Selection: \n")
    print("1 - Register\n")
    print("2 - Login\n")

    user_choice = int(input(("Enter a number: ")))
    
    if user_choice == 1:
        register_user()
    elif user_choice == 2:
        login()

if __name__ == "__main__":
    main()