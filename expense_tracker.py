import calendar
import datetime
from expense import Expense
import expense


def main():
    expense_file_path = "expenses.csv"
    budget = 2000
    # get use input for expense.
    expense = get_user_expense()
    # write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    # read file and summarize expense
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print("Getting User's Expense \n")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    print(f"You've entered {expense_name}, {expense_amount}")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc",
    ]
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}.{category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input("Enter a category number: "))-1
        print(range(len(expense_categories)-1))
        print(selected_index)
        if selected_index in range(len(expense_categories) - 1):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("*** Invalid Category. Please try again. *** \n")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"savings user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"summarizing user expense \n")
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
        print("Expenses by Category: \n")
        print(f" {key}: ${amount:.2f} ")

    total_spent = sum([exp.amount for exp in expenses])
    print(f"You've spent ${total_spent:.2f} this month.")
    remaining_budget = budget - total_spent
    print(f"Your remaining Budget is ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    print("Reamining days in the current month: ", remaining_days)

    daily_budget = remaining_budget / remaining_days

    print(f"Budget per day: ${daily_budget:.2f}")

if __name__ == "__main__":
    main()