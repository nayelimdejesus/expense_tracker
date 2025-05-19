def main():
    print(f"Running Expense Tracker")
    # get use irnput for expense.
    get_user_expense()
    # write their expense to a file
    save_expense_to_file()
    # read file and summarize expense
    summarize_expense()


def get_user_expense():
    print("getting user expense")
    expense_name = input("Enter expense name:")
    expense_amount = float(input("Enter expense amount:"))

    print(f"You've entered {expense_name}, {expense_amount}")

    expense_categories = [
        "Food", "Home", "Work", "Fun", "Misc",
    ]
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}.{category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = input("Enter a category numer: ")
        print(selected_index)
        break

def save_expense_to_file():
    print(f"savings user expense")
      

def summarize_expense():
    print(f"summarizing user expense")
      


    pass

if __name__ == "__main__":
    main()