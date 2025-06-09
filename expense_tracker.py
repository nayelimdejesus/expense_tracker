import calendar
import datetime

from colorama import Fore, Back, Style, init
from expense import Expense
import expense
from db import db

def menu(username):
    while True:
        print("\nWhat would you like to do?")
        print("1 - Add budget\n")
        print("2 - Add expense\n")
        print("3 - Summarize expenses\n")
        try:
            option = int(input("Enter a number: "))
            if option not in [1,2,3]:
                print(Fore.RED + "\nPlease select either 1 or 2.")
                continue
            break
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")

    match option:
        case 1:
            get_user_budget(username)
        case 2:
            get_user_expense()
        case 3: 
            summarize_expenses()
        case _: 
            print("Error")
            
            
            
users_collection = db["users"]
budgets_collection = db["budgets"]
def get_user_budget(username):
    user_budget = float(input("\nEnter your monthly budget: "))
    existing = budgets_collection.find_one({"username": username})
    if existing:

        budgets_collection.update_one(
            {"username": username},
            {"$set": {"budget":user_budget}}
        )
        print(f"Updated budget for {username} to {user_budget}")
    else:
        # Insert new budget
        budgets_collection.insert_one({
            "username": username,
            "budget": user_budget
        })
        print(f"Added budget for {username}: {user_budget:.2f}")
    return user_budget

def get_user_expense():    
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
            print(f"  {i + 1}.{category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input("Enter a category number: "))-1

        if selected_index in range(len(expense_categories) - 1):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("*** Invalid Category. Please try again. *** \n")

def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"\nExpense Summary:")
    expenses = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            expense_name, expense_category, expense_amount = line.strip().split(",")
            line_expense = Expense(
                name= expense_name, 
                category= expense_category, 
                amount= float(expense_amount)
            )
            expenses.append(line_expense)

      
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount


    for key, amount in amount_by_category.items():
        print(f"Expenses by Category:")
        print(f"{key}: ${amount:.2f} ")

    total_spent = sum([exp.amount for exp in expenses])
    print(f"\nYou've spent ${total_spent:.2f} this month.")
    remaining_budget = budget - total_spent
    print(f"Your remaining Budget is ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    print("Remaining days in the current month: ", remaining_days)

    daily_budget = remaining_budget / remaining_days
    warning = budget * .80

    print(warning)
    print(total_spent)
    if total_spent >= warning:
        print("/n**** WARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET ****")

    print(f"Your budget per day: ${daily_budget:.2f}")
