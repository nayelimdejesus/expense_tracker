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
        print("4 - Logout\n")
        print("5 - Exit\n")
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
            case 4:
                print("Logging out now ...")
                return
            case 5:
                print("Exiting program now ...")
                exit(0)
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
        expense_collection.update_one(
            {"username": username},
            {"$set": {"budget_added": True}}
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
                "category": selected_category,
                "date": datetime.datetime.now()
            }

            expense_collection.update_one(
                {"username": username},
                {"$push": {"expenses": new_expense}}
            )

            print(Fore.GREEN + f"Added expense for {username}: {expense_name}, {expense_amount:.2f}, {selected_category}")
            if budget_exist:
                stored_budget = budget_exist.get("budget", 0.0)
                budget = stored_budget - expense_amount
                expense_collection.update_one(
                    {"username": username},
                    {"$set": {"budget": budget}}
                )
            return new_expense

        else:
            print(Fore.RED + "*** Invalid Category. Please try again. *** \n")

def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(username):
    expenses = expense_collection.find_one({"username": username})
    budget_add = expenses.get("budget_added", False)
    
    if not expenses:
        print("No expenses found.")
        return False
    user_expense = expenses.get("expenses", [])

    sum_categories = {}
    # for i in range(0, len(user_expense)):
    #     print(f"\n{user_expense[i]["date"]}")
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
 
    print("\n--------------------------------------")
    
    # Getting dates to get yearly total spent, and monthly total spent
    today = datetime.date.today()
    start_of_month = datetime.date(today.year,today.month,1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    end_of_month = datetime.date(today.year, today.month, last_day)  
    start_of_year = datetime.date(today.year, 1, 1)
    end_of_year = datetime.date(today.year, 12, 31)
    
    # Gets yearly total spent    
    yearly_spent = 0
    for i in range(0, len(user_expense)):
        if start_of_year <= user_expense[i]["date"].date() <= end_of_year:
            yearly_spent += user_expense[i]["amount"]
    print(f"This Year Total Spent: ${yearly_spent:.2f}")
    
    # Gets monthly total spent
    monthly_spent = 0
    for i in range(0, len(user_expense)):
        if start_of_month <= user_expense[i]["date"].date() <= end_of_month:
            monthly_spent += user_expense[i]["amount"]
    print(f"This Month Total Spent: ${monthly_spent:.2f}")
        
    if not budget_add:
        print("Remaining Budget: No Budget Added")
    else:
        remaining_budget = expenses.get("budget", 0.0)
        print(f"Remaining Budget: ${remaining_budget:.2f}")
        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day
        daily_budget = remaining_budget / remaining_days
        # print(f"Daily Budget: ${daily_budget:.2f}")
        daily_budget = remaining_budget / remaining_days
        warning = remaining_budget * .80

        if total_amount >= warning:
            print(Fore.RED +"WARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET")
    