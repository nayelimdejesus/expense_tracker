import calendar
import datetime

from colorama import Fore, Back, Style, init
from expense import Expense
import expense
from db import db

def menu(username):
    # Menu options that display after user logs in
    while True:
        print(Fore.LIGHTCYAN_EX + "\nWhat would you like to do?")
        print(Fore.LIGHTMAGENTA_EX +"1 - Add Budget\n")
        print(Fore.LIGHTMAGENTA_EX +"2 - Add Expense\n")
        print(Fore.LIGHTMAGENTA_EX +"3 - Delete Expense\n")
        print(Fore.LIGHTMAGENTA_EX +"4 - View Expense Summary\n")
        print(Fore.LIGHTMAGENTA_EX +"5 - Logout\n")
        print(Fore.LIGHTMAGENTA_EX +"6 - Exit\n")
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
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Adding Expense ======")
                get_user_expense(username)
            case 3:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Delete Expense ======")
                delete_expense(username)
            case 4: 
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Expense Summary ======")
                summarize_expenses(username)
            case 5:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT+"Logged out")
                return
            case 6:
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
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Updating Budget ======")
        existing_budget = existing.get("monthly_budget", 0.0)
        existing_remaining = existing.get("remaining_budget", 0.0)
        expenses_entries = existing.get("expenses", [])
        print(Fore.LIGHTMAGENTA_EX + f"Monthly budget is set to ${existing_budget:.2f}")
        print(Fore.LIGHTMAGENTA_EX + f"Remaining budget is currently ${existing_remaining:.2f}")
        
        print(Fore.LIGHTYELLOW_EX + "\nTo return to main menu, press 'q'.")
        while True:
            try:
                user_budget = (input("\nEnter your new monthly budget: "))
                if user_budget.lower() == "q":
                    return 
                new_budget = float(user_budget)
                if new_budget <= 0:
                    print(Fore.RED + "Budget must be greater than 0. Please try again.")
                    continue
                # if the user has expenses for this month, add up all amounts of this month then subtract it from the budget that was added.
                # update the database after the calculation
                if expenses_entries:
                    diff = existing_budget - existing_remaining
                    updated_remaining = new_budget - diff
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"monthly_budget": new_budget}}
                    )
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"remaining_budget": updated_remaining}}
                    )
                    break
                else:
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"monthly_budget": new_budget}}
                    )
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"remaining_budget": new_budget}}
                    )
                    break
            except ValueError:
                print(Fore.RED + f"\nEnter a valid amount. Please try again.")

        print(Fore.YELLOW + f"\nUpdated budget to {new_budget:.2f}")

    else:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT+ "\n====== Adding Budget ======")
        while True:
            try:
                user_budget = float(input("Enter your monthly budget: "))
                if user_budget <= 0:
                    print(Fore.RED + "\nBudget must be greater than 0. Please try again.")
                    continue
                expense_collection.insert_one({
                    "username": username,
                    "monthly_budget": user_budget,
                    "remaining_budget":user_budget,
                    "expenses": []
                    })
                print(Fore.YELLOW + f"\nMonthly budget set to: ${user_budget:.2f}")
                break
            except ValueError:
                print(Fore.RED + f"\nEnter a valid amount. Please try again.")

                
    return user_budget


def delete_expense(username):
    expenses = expense_collection.find_one({"username": username})
    
    # If the user has not added any expenses, display "No expenses found"
    if expenses and expenses.get("expenses"):
        expenses_entries = expenses.get("expenses", [])
        
        print(Fore.LIGHTYELLOW_EX + "To return to main menu, press 'q'.\n")
        while True:
            print(Fore.LIGHTCYAN_EX + "Select an expense to delete: ")
            for i, k in enumerate(expenses_entries):
                date_obj = k["date"]
                date_format = date_obj.strftime("%Y-%m-%d")
                print( f"{i + 1} - Date Added: {date_format}, {k["category"]}", f"{k["name"]}", f"${k['amount']:.2f}")
            try:
                selected_index = input("\nEnter a number: ")

                if selected_index == "q":
                    return
                deleted_index = int(selected_index) -1
                
                if deleted_index in range(len(expenses_entries)):
                    # the expense the user selected
                    
                    selected_expense = expenses_entries[deleted_index]
                    expense_name = selected_expense["name"]
                    expense_amount = selected_expense["amount"]
                    expense_category = selected_expense["category"]
                    
                    
                    del expenses_entries[deleted_index]
                    
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"expenses": expenses_entries}}
                    )
            
                    print(Fore.YELLOW+ f"\nDeleted Expense: {expense_category}, {expense_name}, ${expense_amount:.2f}")
                    remaining_budget = expenses.get("remaining_budget", 0.0)
                    new_remaining = remaining_budget + expense_amount
                
                    # Update the budget value in the database with the expense amount that was deleted.
                    expense_collection.update_one(
                        {"username": username},
                        {"$set": {"remaining_budget": new_remaining}}
                    )
                    return
                else:
                    print(Fore.RED + "\nPlease enter a valid number.")
            except ValueError:
                print(Fore.RED + "\nPlease enter a valid number.")
                continue

    else:
        print(f"No expenses found.")
        return
         


# Get's users expense information like: expense name, expense amount, category
def get_user_expense(username):
    budget_exist = expense_collection.find_one({"username": username})
    
    # if user did not add a budget it'll tell them to add one
    if not budget_exist:
        print(Fore.LIGHTRED_EX + "You must add a budget before adding an expense.")
        return
    
    print(Fore.LIGHTYELLOW_EX + "To return to main menu, press 'q'.\n")

    expense_name = input("Enter expense name: ")
    
    if expense_name == "q":
        return
    # expense_amount = float(input("Enter expense amount: "))
    
    while True: 
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount > 0:
                break
            else:
                print(Fore.RED + "\nExpense amount must be greater than 0.")
        except ValueError:
            print(Fore.RED + "\nPlease enter a valid amount")
            continue
    
    # # Displays expense name, and amount that user had entered
    # print(Fore.YELLOW + Style.BRIGHT + f"\nYou've entered the following:" )
    # print(Fore.LIGHTYELLOW_EX + f"Expense Name: {expense_name}")
    # print(Fore.LIGHTYELLOW_EX + f"Expense Amount: {expense_amount:.2f}\n")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc", "Travel"
    ]
    
    # Prompts user to select an expense category
    while True:
        print(Fore.LIGHTCYAN_EX + "\nSelect a category: ")
        for i, category_name in enumerate(expense_categories):
            print(Fore.LIGHTMAGENTA_EX + f"{i + 1}.{category_name}\n")
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

            print(Fore.YELLOW + f"\nExpense added: {selected_category}, {expense_name}, ${expense_amount:.2f}")
            
            stored_remaining = budget_exist.get("remaining_budget", 0.0)
            # Subtract the expense amount from the current budget
            new_remaining = stored_remaining - expense_amount
            # Update the budget value in the database with the new amount
            expense_collection.update_one(
                {"username": username},
                {"$set": {"remaining_budget": new_remaining}}
            )
            print(Fore.YELLOW + f"Remaining budget: ${new_remaining}")
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
        print(Fore.YELLOW+ f"{i + ':':<18} ${k:>7.2f}")
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
    print(Fore.YELLOW +f"{'This Year:':<18} ${yearly_spent:>7.2f}")
    
    # Gets monthly total spent
    monthly_spent = 0
    for i in range(0, len(user_expense)):
        if start_of_month <= user_expense[i]["date"].date() <= end_of_month:
            monthly_spent += user_expense[i]["amount"]
    print(Fore.YELLOW +f"{'This Month:':<18} ${monthly_spent:>7.2f}")

    remaining_budget = expenses.get("remaining_budget", 0.0)
    print(Fore.YELLOW +f"{'Remaining Budget:':<18} ${remaining_budget:>7.2f}")
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days
    # 80% of budget
    warning = remaining_budget * .80

    if total_amount >= warning:
        print(Fore.RED +"\nWARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET")
        
    