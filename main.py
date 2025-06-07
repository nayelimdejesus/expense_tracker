import os
from auth import register_user

def main():
    print("Welcome to the Expense App\n")
    print("Please make a selection:\n")
    print("1 - Register\n")
    print("2 - Login\n")

    user_choice = int(input(("Enter a number: ")))
    
    if user_choice == 1:
        register_user()




if __name__ == "__main__":
    main()