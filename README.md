# Personal Expense Tracker

Add, view, search and delete expenses. Data stored in JSON.

## Run
    python cli.py     # terminal version
    flet run          # mobile/desktop UI (pip install -U flet)

## Build the Android APK
    flet build apk -v
or push to GitHub and download the APK from the *Actions* tab.

## Structure
- `expense.py`  – Expense class (OOP)
- `storage.py`  – JSON load/save, CSV export (file handling + exceptions)
- `tracker.py`  – ExpenseTracker logic (lists, dicts, loops)
- `cli.py`      – terminal menu
- `main.py`     – Flet UI (entry point for the Android app)
