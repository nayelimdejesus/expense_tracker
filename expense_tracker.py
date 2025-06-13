import calendar
import datetime 

from colorama import Fore, Back, Style, init
from expense import Expense
import expense
from db import db

def menu(username):
    # Menu options that display after user logs in
    while True:
        print(Fore.LIGHTYELLOW_EX + "\nWhat would you like to do?")
        print("1 - Add Budget\n")
        print("2 - Add Expense\n")
        print("3 - View Expense Summary\n")
        print("4 - Logout\n")
        print("5 - Exit\n")
        try:
            option = int(input("Enter a number: "))
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue

        # Based on the user's menu selection, it calls the corresponding function
        match option:
            case 1:
                get_user_budget(username)
            case 2:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\nAdding Expense")
                get_user_expense(username)
            case 3: 
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Expense Summary ======")
                summarize_expenses(username)
            case 4:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+"Logged out")
                return
            case 5:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+"Goodbye.")
                exit(0)
            case _: 
                print(Fore.RED + "\nPlease enter a valid number.")
            
            
            
users_collection = db["users"]
expense_collection = db["expenses"]

# Gets the user's monthly budget
def get_user_budget(username):
    existing = expense_collection.find_one({"username": username})
    if existing: 
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\nUpdating Budget")
        existing_budget = existing.get("budget", 0.0)
        print(Fore.LIGHTMAGENTA_EX + f"Your current budget is set to ${existing_budget:.2f}")
        user_budget = float(input("\nEnter your new monthly budget: "))
        expense_collection.update_one(
            {"username": username},
            {"$set": {"budget": user_budget}}
        )
        print(Fore.LIGHTGREEN_EX + f"\nUpdated budget to {user_budget}")

    else:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\nAdding Budget")
        user_budget = float(input("Enter your monthly budget: "))
        expense_collection.insert_one({
            "username": username,
            "budget": user_budget,
            "expenses": []
            })
        print(Fore.GREEN + f"Added budget for {username}: ${user_budget:.2f}")
    return user_budget

# Get's users expense information like: expense name, expense amount, category
def get_user_expense(username):
    budget_exist = expense_collection.find_one({"username": username})
    
    # if user did not add a budget it'll tell them to add one
    if not budget_exist:
        print(Fore.LIGHTRED_EX + "You must add a budget before adding an expense.")
        return
    
    expense_name = input("Enter expense name: ")
    # expense_amount = float(input("Enter expense amount: "))
    
    while True: 
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount:
                break
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid amount")
            continue
    
    # Displays expense name, and amount that user had entered
    print(f"\nYou've entered the following:" )
    print(f"Expense Name: {expense_name}")
    print(f"Expense Amount: {expense_amount:.2f}\n")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc", "Travel"
    ]
    
    # Prompts user to select an expense category
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}.{category_name}")
        try:
            selected_index = int(input("Enter a category number: ")) - 1
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid number.")
            continue
  
        # if the selected category is valid then it'll create a new expense
        if selected_index in range(len(expense_categories)):
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
                # Subtract the expense amount from the current budget
                budget = stored_budget - expense_amount
                # Update the budget value in the database with the new amount
                expense_collection.update_one(
                    {"username": username},
                    {"$set": {"budget": budget}}
                )
            return new_expense

        else:
            print(Fore.RED + "*** Invalid Category. Please try again. *** \n")

# def save_expense_to_file(expense: Expense, expense_file_path):
#     with open(expense_file_path, "a") as f:
#         f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(username):
    expenses = expense_collection.find_one({"username": username})
    
    # If the user has not added any expenses, display "No expenses found"
    if not expenses or not expenses.get("expenses"):
        print("No expenses found.")
        return False
    user_expense = expenses.get("expenses", [])

    # Add the expenses amount based on category
    sum_categories = {}
    for i in range(0, len(user_expense)):
        key = user_expense[i]["category"]
        if key in sum_categories:
            sum_categories[key] += user_expense[i]["amount"]
        else:
            sum_categories[key] = user_expense[i]["amount"]
    total_amount = 0.0
    print("Categories:")
    for i, k in sum_categories.items():
        print(Fore.LIGHTMAGENTA_EX + f"{i + ':':<18} ${k:>7.2f}")
        total_amount += k
 
    print("\n--------------------------------------")
    print("Totals:")
    
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
    print(Fore.LIGHTMAGENTA_EX +f"{'This Year:':<18} ${yearly_spent:>7.2f}")
    
    # Gets monthly total spent
    monthly_spent = 0
    for i in range(0, len(user_expense)):
        if start_of_month <= user_expense[i]["date"].date() <= end_of_month:
            monthly_spent += user_expense[i]["amount"]
    print(Fore.LIGHTMAGENTA_EX +f"{'This Month:':<18} ${monthly_spent:>7.2f}")

    remaining_budget = expenses.get("budget", 0.0)
    print(Fore.LIGHTMAGENTA_EX +f"{'Remaining Budget:':<18} ${remaining_budget:>7.2f}")
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days
    # 80% of budget
    warning = remaining_budget * .80

    if total_amount >= warning:
        print(Fore.RED +"\nWARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET")
        
    