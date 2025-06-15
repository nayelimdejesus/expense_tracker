import os
from auth import register_user, login
from expense_tracker import menu
from colorama import Fore, Back, Style, init


def main():
    # List options for user to choose
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "Welcome to the Expense App")
    while True:
        print(Fore.LIGHTCYAN_EX +"\nMake a Selection:")
        print(Fore.LIGHTMAGENTA_EX + "1 - Register\n")
        print(Fore.LIGHTMAGENTA_EX +"2 - Login\n")
        print(Fore.LIGHTMAGENTA_EX +"3 - Exit\n")
        try:
            user_choice = int(input("Enter a number: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue
        
        # Based on the user's menu selection, it calls the corresponding function
        match user_choice:
            case 1:
                register_user()
            case 2:
                username = login()
                if username:
                    menu(username)
                else:
                    continue
            case 3:
                print(Fore.LIGHTGREEN_EX+"Goodbye.")                
                exit(0)
            case _:
                print(Fore.RED + "\nPlease enter a valid number.")
            
            


if __name__ == "__main__":
    main()