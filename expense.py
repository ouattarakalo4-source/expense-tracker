"""OOP: one Expense = one object."""
from datetime import date


class Expense:
    def __init__(self, expense_id, amount, category, description, expense_date=None):
        self.id = expense_id
        self.amount = float(amount)
        self.category = category.strip().lower()
        self.description = description.strip()
        self.date = expense_date or date.today().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["amount"], data["category"],
                   data["description"], data["date"])

    def __str__(self):
        return (f"#{self.id:<3} {self.date}  {self.amount:>10.2f}  "
                f"{self.category:<12} {self.description}")
