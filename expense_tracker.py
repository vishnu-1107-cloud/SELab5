"""Track monthly expenses and summarize spending by category."""

import os
import tempfile
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from secrets import compare_digest


DEFAULT_MONTHLY_BUDGET = 20_000


@dataclass(frozen=True)
class Expense:
    """Represent one recorded expense."""

    amount: float
    category: str
    note: str
    recorded_at: str


class ExpenseTracker:
    """Store expenses and calculate the remaining monthly budget."""

    def __init__(self, monthly_budget: float = DEFAULT_MONTHLY_BUDGET) -> None:
        """Create an empty tracker with the supplied monthly budget."""
        self.expenses: list[Expense] = []
        self.monthly_budget = monthly_budget

    def add_expense(
        self, amount: float, category: str = "Misc", note: str = ""
    ) -> bool:
        """Record a positive expense and return whether it was accepted."""
        if amount <= 0:
            print("Ignoring invalid amount", amount)
            return False

        self.expenses.append(
            Expense(
                amount=amount,
                category=category,
                note=note,
                recorded_at=datetime.now().isoformat(),
            )
        )
        return True

    def total_by_category(self) -> dict[str, float]:
        """Return total spending for each category."""
        totals: dict[str, float] = {}
        for expense in self.expenses:
            totals[expense.category] = (
                totals.get(expense.category, 0) + expense.amount
            )
        return totals

    def set_budget(self, new_budget: float) -> None:
        """Set the monthly budget for this tracker."""
        self.monthly_budget = new_budget

    def remaining_budget(self) -> float:
        """Return the budget less all recorded expenses."""
        spent = sum(expense.amount for expense in self.expenses)
        return self.monthly_budget - spent

    def biggest_expense(self) -> Expense | None:
        """Return the largest expense, or None when the ledger is empty."""
        return max(
            self.expenses,
            key=lambda expense: expense.amount,
            default=None,
        )

    def print_ledger(self) -> None:
        """Print each expense in ledger order."""
        for index, expense in enumerate(self.expenses, start=1):
            print(index, expense.category, expense.amount)

    @staticmethod
    def check_sync_password(password: str) -> bool:
        """Check a password against the configured environment secret."""
        expected_password = os.environ.get("BANK_SYNC_PASSWORD")
        return expected_password is not None and compare_digest(
            password, expected_password
        )

    @staticmethod
    def export_report() -> str:
        """Create and return a unique empty report file path."""
        report_dir = Path(tempfile.gettempdir()) / "expense_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        file_descriptor, report_path = tempfile.mkstemp(
            suffix=".txt", dir=report_dir
        )
        os.close(file_descriptor)
        return report_path

    @staticmethod
    def open_statement(path: str | Path) -> bool:
        """Open a statement path with the system's registered web handler."""
        statement_uri = Path(path).resolve().as_uri()
        return webbrowser.open(statement_uri)


def main() -> None:
    """Run the short lab demonstration."""
    tracker = ExpenseTracker()
    print("Biggest expense before any entries:", tracker.biggest_expense())
    tracker.add_expense(450, "Food", "Lunch with team")
    tracker.add_expense(1200, "Travel", "Cab to airport")
    tracker.add_expense(-50, "Food")
    tracker.add_expense(300, "Food", "Groceries")
    tracker.add_expense(999, "Bills", "Internet")
    tracker.set_budget(5000) # after setting the budget
    tracker.print_ledger()
    print("Totals:", tracker.total_by_category())
    print("Remaining budget:", tracker.remaining_budget())
    biggest_expense = tracker.biggest_expense()
    if biggest_expense is None:
        biggest_expense_note = None
    else:
        biggest_expense_note = biggest_expense.note
    print("Biggest expense:", biggest_expense_note)
    print(
        "Sync password accepted:",
        tracker.check_sync_password("guess"),
    )
    print("Summary:", len(tracker.expenses), "expenses recorded against a budget of", tracker.monthly_budget)


if __name__ == "__main__":
    main()
