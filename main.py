import os
from auth import register_user, login
from expense_tracker import get_user_budget, get_user_expense, summarize_expenses

def main():
    print("Welcome to the Expense App\n")
    print("Make a Selection: \n")
    print("1 - Register\n")
    print("2 - Login\n")

    user_choice = int(input(("Enter a number: ")))
    
    if user_choice == 1:
        register_user()
    elif user_choice == 2:
        while True:
            print("\n*** Login ***")
            username = input("Enter username: ")
            pwd = input("Enter password: ")
            if login(username, pwd):
                break
        print("What would you like to do?")
        print("1 - Add budget\n")
        print("2 - Add expense\n")
        print("3 - Summarize expenses\n")

        option = int(input("Enter a number: "))

        match option:
            case 1:
                get_user_budget(username)
            case 2:
                get_user_expense()
            case 3: 
                summarize_expenses()
            case _: 
                print("Error")


if __name__ == "__main__":
    main()