"""File handling: JSON for storage, CSV for export. Exceptions handled here."""
import csv
import json
import os

from expense import Expense

DATA_FILE = os.path.join("data", "expenses.json")


def load_expenses(path=DATA_FILE):
    """Return a list of Expense objects. Empty list if file missing/corrupted."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [Expense.from_dict(d) for d in json.load(f)]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, ValueError):
        print("⚠️  Data file is corrupted. Starting with an empty list.")
        return []


def save_expenses(expenses, path=DATA_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2, ensure_ascii=False)


def export_csv(expenses, path="expenses.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "amount", "category", "description", "date"])
        writer.writeheader()
        for e in expenses:
            writer.writerow(e.to_dict())
    return path
