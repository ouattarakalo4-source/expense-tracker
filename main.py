"""Mobile/desktop UI (Flet). Run: flet run  |  Build: flet build apk"""
import flet as ft

from storage import load_expenses, save_expenses
from tracker import ExpenseTracker


def main(page: ft.Page):
    page.title = "Expense Tracker"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    tracker = ExpenseTracker(load_expenses())

    amount = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    category = ft.TextField(label="Category (food, transport...)", expand=True)
    description = ft.TextField(label="Description")
    search = ft.TextField(label="Search", prefix_icon=ft.Icons.SEARCH)
    message = ft.Text()
    total_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
    categories_text = ft.Text(size=13)
    expense_list = ft.Column(spacing=4)

    def refresh():
        keyword = (search.value or "").strip()
        items = tracker.search(keyword) if keyword else tracker.expenses
        items = sorted(items, key=lambda e: (e.date, e.id), reverse=True)

        total_text.value = f"Total: {tracker.total():,.0f}"
        by_category = tracker.totals_by_category()
        categories_text.value = "  ·  ".join(
            f"{name}: {value:,.0f}" for name, value in sorted(by_category.items())
        ) or "No expenses yet"
        expense_list.controls = [make_row(e) for e in items] or [ft.Text("No expenses found.")]
        page.update()

    def make_row(e):
        return ft.Card(
            content=ft.ListTile(
                title=ft.Text(f"{e.description or e.category}  —  {e.amount:,.0f}"),
                subtitle=ft.Text(f"{e.date}  ·  {e.category}"),
                trailing=ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda _, expense_id=e.id: delete_expense(expense_id),
                ),
            )
        )

    def add_expense(_):
        try:
            tracker.add(
                float((amount.value or "").replace(",", ".")),
                category.value or "other",
                description.value or "",
            )
        except ValueError:
            message.value = "Enter a valid positive amount."
            message.color = ft.Colors.RED
            page.update()
            return
        save_expenses(tracker.expenses)
        amount.value = ""
        description.value = ""
        message.value = "Added ✓"
        message.color = ft.Colors.GREEN
        refresh()

    def delete_expense(expense_id):
        if tracker.delete(expense_id):
            save_expenses(tracker.expenses)
            message.value = "Deleted ✓"
            message.color = ft.Colors.GREEN
        refresh()

    search.on_change = lambda _: refresh()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Text("Expense Tracker", size=28, weight=ft.FontWeight.BOLD),
                    total_text,
                    categories_text,
                    ft.Divider(),
                    ft.Row([amount, category]),
                    description,
                    ft.Button("Add expense", icon=ft.Icons.ADD, on_click=add_expense),
                    message,
                    ft.Divider(),
                    search,
                    expense_list,
                ]
            )
        )
    )
    refresh()


ft.run(main)
