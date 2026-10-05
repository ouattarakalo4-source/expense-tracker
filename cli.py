"""Terminal menu. Run: python cli.py"""
from datetime import datetime

from storage import export_csv, load_expenses, save_expenses
from tracker import ExpenseTracker

MENU = """
===== PERSONAL EXPENSE TRACKER =====
1. Add expense
2. View all expenses
3. Search
4. Delete expense
5. Summary by category
6. Export to CSV
0. Quit
"""


def show(expenses):
    if not expenses:
        print("No expenses found.")
        return
    for e in sorted(expenses, key=lambda x: x.date):
        print(e)


def ask_amount():
    while True:
        try:
            value = float(input("Amount: ").replace(",", "."))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("❌ Enter a positive number.")


def ask_date():
    while True:
        raw = input("Date (YYYY-MM-DD, Enter = today): ").strip()
        if not raw:
            return None
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("❌ Invalid date format.")


def add_expense(tracker):
    amount = ask_amount()
    category = input("Category (food, transport...): ") or "other"
    description = input("Description: ")
    expense = tracker.add(amount, category, description, ask_date())
    print(f"✅ Added: {expense}")


def delete_expense(tracker):
    try:
        expense_id = int(input("ID to delete: "))
    except ValueError:
        print("❌ ID must be a number.")
        return
    print("✅ Deleted." if tracker.delete(expense_id) else "❌ ID not found.")


def summary(tracker):
    for category, total in sorted(tracker.totals_by_category().items()):
        print(f"{category:<15} {total:>10.2f}")
    print(f"{'TOTAL':<15} {tracker.total():>10.2f}")


def main():
    tracker = ExpenseTracker(load_expenses())
    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice == "1":
            add_expense(tracker)
        elif choice == "2":
            show(tracker.expenses)
        elif choice == "3":
            show(tracker.search(input("Keyword: ")))
        elif choice == "4":
            delete_expense(tracker)
        elif choice == "5":
            summary(tracker)
        elif choice == "6":
            print(f"✅ Exported to {export_csv(tracker.expenses)}")
        elif choice == "0":
            save_expenses(tracker.expenses)
            print("Saved. Bye!")
            break
        else:
            print("❌ Invalid choice.")
        save_expenses(tracker.expenses)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
