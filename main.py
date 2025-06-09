import os
from auth import register_user, login
from expense_tracker import menu
from colorama import Fore, Back, Style, init


def main():
    print("Welcome to the Expense App\n")
    while True:
        print("Make a Selection:")
        print("1 - Register\n")
        print("2 - Login\n")
        try:
            user_choice = int(input("Enter a number: "))
            if user_choice not in [1,2]:
                print(Fore.RED + "\nPlease select either 1 or 2.")
                continue
            break
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")

    match user_choice:
        case 1:
            register_user()
            while True:
                print("\nWould you like to login?:")
                print("1 - Yes\n")
                print("2 - No\n")
                try:
                    option = int(input("Enter a number: "))
                    if option not in [1,2]:
                        print(Fore.RED + "\nPlease select either 1 or 2.")
                        continue
                    break
                except ValueError:
                    print(Fore.RED + "\nPlease enter a valid number.")
            if option == 1:
                username = login()
                menu(username)
            else:
                return False
        case 2:
            username = login()
            menu(username)


if __name__ == "__main__":
    main()