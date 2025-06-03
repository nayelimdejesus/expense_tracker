from expense import Expense


def main():
    # get use input for expense.
    expense = get_user_expense()
    print(expense)
    # write their expense to a file
    save_expense_to_file()
    # read file and summarize expense
    summarize_expense()


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

def save_expense_to_file():
    print(f"savings user expense")
      

def summarize_expense():
    print(f"summarizing user expense")
      


    pass

if __name__ == "__main__":
    main()