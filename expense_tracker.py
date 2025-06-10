import calendar
import datetime

from colorama import Fore, Back, Style, init
from expense import Expense
import expense
from db import db

def menu(username):
    while True:
        print(Fore.LIGHTYELLOW_EX + "\nWhat would you like to do?")
        print("1 - Add budget\n")
        print("2 - Add expense\n")
        print("3 - Summarize expenses\n")
        try:
            option = int(input("Enter a number: "))
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue

        match option:
            case 1:
                print(Fore.LIGHTYELLOW_EX+ "\nUpdating / Adding Budget")
                get_user_budget(username)
            case 2:
                print(Fore.LIGHTYELLOW_EX+ "\nAdding Expense")
                get_user_expense(username)
            case 3: 
                print(Fore.LIGHTYELLOW_EX+ "\nSummarizing Expense")
                summarize_expenses(username)
            case _: 
                print(Fore.RED + "\nPlease enter a valid number.")
            
            
            
users_collection = db["users"]
expense_collection = db["expenses"]


def get_user_budget(username):
    user_budget = float(input("\nEnter your monthly budget: "))
    existing = expense_collection.find_one({"username": username})
    if existing:
        expense_collection.update_one(
            {"username": username},
            {"$set": {"budget": user_budget}}
        )
        print(f"Updated budget for {username} to {user_budget}")
    else:
        expense_collection.insert_one({
            "username": username,
            "budget": user_budget,
            "budget_added":True,
            "expenses": []
            })
        print(Fore.GREEN + f"Added budget for {username}: {user_budget:.2f}")
    return user_budget

def get_user_expense(username):
    budget_exist = expense_collection.find_one({"username": username})
    if not budget_exist:
        expense_collection.insert_one({
        "username": username,
        "budget": 0.0,
        "budget_added": False,
        "expenses": []
    })
        
    expense_name = input("\nEnter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    print(f"\nYou've entered the following:" )
    print(f"Expense Name: {expense_name}")
    print(f"Expense Amount: {expense_amount:.2f}\n")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc", "Travel"
    ]
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}.{category_name}")
        try:
            selected_index = int(input("Enter a category number: "))
            selected_index -=1
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue
  
        # print(range(len(expense_categories)-1))
        if selected_index in range(len(expense_categories)-1):
            selected_category = expense_categories[selected_index]
            new_expense = {
                "name": expense_name,
                "amount": expense_amount,
                "category": selected_category
            }

            expense_collection.update_one(
                {"username": username},
                {"$push": {"expenses": new_expense}}
            )

            print(Fore.GREEN + f"Added expense for {username}: {expense_name}, {expense_amount:.2f}, {selected_category}")
            return new_expense

        else:
            print(Fore.RED + "*** Invalid Category. Please try again. *** \n")

def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(username):
    expenses = expense_collection.find_one({"username": username})
    if not expenses:
        print("No expenses found.")
        return False
    user_expense = expenses.get("expenses", [])
    # budget = {expenses.get("budget", 0.0)}
    # budget_left = budget

    sum_categories = {}
    for i in range(0, len(user_expense)):
        key = user_expense[i]["category"]
        if key in sum_categories:
            sum_categories[key] += user_expense[i]["amount"]
        else:
            sum_categories[key] = user_expense[i]["amount"]
    total_amount = 0.0
    for i, k in sum_categories.items():
        print(f"{i}: ${k:.2f}")
        total_amount += k
 
    print(f"\nBudget: {expenses.get("budget", 0.0)}")
    print(f"Total amount spent: {total_amount:.2f}")
    
        
    
    

    # total_spent = sum([exp.amount for exp in expenses])
    # print(f"\nYou've spent ${total_spent:.2f} this month.")
    # remaining_budget = budget - total_spent
    # print(f"Your remaining Budget is ${remaining_budget:.2f}")

    # now = datetime.datetime.now()
    # days_in_month = calendar.monthrange(now.year, now.month)[1]
    # remaining_days = days_in_month - now.day

    # print("Remaining days in the current month: ", remaining_days)

    # daily_budget = remaining_budget / remaining_days
    # warning = budget * .80

    # print(warning)
    # print(total_spent)
    # if total_spent >= warning:
    #     print("/n**** WARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET ****")

    # print(f"Your budget per day: ${daily_budget:.2f}")
