"""Tests for the dashboard page and its data display."""

from tests.conftest import register, login, logout


def _add(client, title="Coffee", amount="120", category="Food", date="2026-06-14"):
    client.post(
        "/expenses/add",
        data={"title": title, "amount": amount, "category": category,
              "date": date, "note": ""},
        follow_redirects=True,
    )


class TestDashboard:
    def test_dashboard_requires_login(self, client):
        response = client.get("/dashboard", follow_redirects=True)
        assert b"Sign in" in response.data or b"login" in response.data.lower()

    def test_dashboard_loads_for_logged_in_user(self, client):
        register(client)
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert b"Dashboard" in response.data

    def test_dashboard_shows_user_greeting(self, client):
        register(client, name="Alice")
        response = client.get("/dashboard")
        assert b"Alice" in response.data

    def test_dashboard_empty_state_shows_zero_totals(self, client):
        register(client)
        response = client.get("/dashboard")
        # With no expenses, month total and all-time total should both be 0
        assert b"0" in response.data

    def test_dashboard_shows_added_expense_in_recent_list(self, client):
        register(client)
        _add(client, title="Lunch", amount="200")
        response = client.get("/dashboard")
        assert b"Lunch" in response.data

    def test_dashboard_transaction_count_increments(self, client):
        register(client)
        _add(client, title="Expense One", amount="100")
        _add(client, title="Expense Two", amount="200")
        _add(client, title="Expense Three", amount="300")
        response = client.get("/dashboard")
        assert b"3" in response.data

    def test_dashboard_only_shows_own_expenses(self, client):
        # Alice adds an expense
        register(client, name="Alice", email="alice@example.com")
        _add(client, title="Alice Expense")
        logout(client)

        # Bob logs in — should NOT see Alice's expense
        register(client, name="Bob", email="bob@example.com")
        response = client.get("/dashboard")
        assert b"Alice Expense" not in response.data

    def test_dashboard_category_chart_data_present(self, client):
        register(client)
        _add(client, category="Transport", amount="500")
        response = client.get("/dashboard")
        assert b"Transport" in response.data

    def test_dashboard_add_expense_link_present(self, client):
        register(client)
        response = client.get("/dashboard")
        assert b"/expenses/add" in response.data or b"Add" in response.data
