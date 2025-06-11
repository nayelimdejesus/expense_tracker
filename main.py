import os
from auth import register_user, login
from expense_tracker import menu
from colorama import Fore, Back, Style, init


def main():
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "Welcome to the Expense App")
    while True:
        print(Fore.LIGHTYELLOW_EX +"\nMake a Selection:")
        print("1 - Register\n")
        print("2 - Login\n")
        print("3 - Exit\n")
        try:
            user_choice = int(input("Enter a number: "))
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue

        match user_choice:
            case 1:
                register_user()
                while True:
                    print(Fore.LIGHTYELLOW_EX +"\nWould you like to login?:")
                    print("1 - Yes\n")
                    print("2 - No\n")
                    try:
                        option = int(input("Enter a number: "))
                    except ValueError:
                        print(Fore.RED + "\nPlease enter a valid number.")
                        continue
                    match option:
                        case 1: 
                            username = login()
                            menu(username)
                        case 2:
                            return False
                        case _:
                            print(Fore.RED + "\nPlease enter a valid number.")
            case 2:
                username = login()
                menu(username)
            case 3:
                print(Fore.LIGHTGREEN_EX+"Goodbye.")                
                exit(0)
            case _:
                print(Fore.RED + "\nPlease enter a valid number.")
            
            


if __name__ == "__main__":
    main()