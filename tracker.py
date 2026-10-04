"""Business logic: lists, dictionaries, loops, functions."""
from expense import Expense


class ExpenseTracker:
    def __init__(self, expenses=None):
        self.expenses = expenses or []

    def _next_id(self):
        return max((e.id for e in self.expenses), default=0) + 1

    def add(self, amount, category, description, expense_date=None):
        if float(amount) <= 0:
            raise ValueError("Amount must be positive.")
        expense = Expense(self._next_id(), amount, category, description, expense_date)
        self.expenses.append(expense)
        return expense

    def delete(self, expense_id):
        for e in self.expenses:
            if e.id == expense_id:
                self.expenses.remove(e)
                return True
        return False

    def search(self, keyword):
        keyword = keyword.lower()
        return [e for e in self.expenses
                if keyword in e.description.lower() or keyword in e.category]

    def total(self):
        return sum(e.amount for e in self.expenses)

    def totals_by_category(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals
