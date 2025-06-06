import calendar
import datetime
from expense import Expense
import expense


def main():
    expense_file_path = "expenses.csv"
    #get user's budget
    budget = get_user_budget()
    # get user's input for expense.
    expense = get_user_expense()
    # write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    # read file and summarize expense
    summarize_expenses(expense_file_path, budget)


def get_user_budget():
    # print("\nGetting User's Budget")
    print("Welcome to the Expense App\n")
    user_budget = float(input("\nEnter your monthly budget: "))
    return user_budget

def get_user_expense():    
    expense_name = input("\nEnter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    print(f"\nYou've entered the following:" )
    print(f"Expense Name: {expense_name}")
    print(f"Expense Amount: {expense_amount:.2f}\n")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc",
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
        print("**** WARNING: YOU'VE SPENT MORE THAN 80% OF YOUR BUDGET ****")

    print(f"Your budget per day: ${daily_budget:.2f}")

if __name__ == "__main__":
    main()