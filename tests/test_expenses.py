"""Tests for add, edit, and delete expense flows."""

from tests.conftest import register, login, logout


def _add(client, title="Coffee", amount="120", category="Food",
         date="2026-06-14", note=""):
    return client.post(
        "/expenses/add",
        data={"title": title, "amount": amount, "category": category,
              "date": date, "note": note},
        follow_redirects=True,
    )


# ── Add expense ───────────────────────────────────────────────────────────────

class TestAddExpense:
    def test_add_requires_login(self, client):
        response = client.get("/expenses/add", follow_redirects=True)
        assert b"Sign in" in response.data or b"login" in response.data.lower()

    def test_add_success_redirects_to_dashboard(self, client):
        register(client)
        response = _add(client)
        assert response.status_code == 200
        assert b"Coffee" in response.data

    def test_add_missing_title_shows_error(self, client):
        register(client)
        response = _add(client, title="")
        assert b"Title is required" in response.data

    def test_add_missing_amount_shows_error(self, client):
        register(client)
        response = _add(client, amount="")
        assert b"Amount is required" in response.data

    def test_add_zero_amount_shows_error(self, client):
        register(client)
        response = _add(client, amount="0")
        assert b"positive" in response.data.lower()

    def test_add_negative_amount_shows_error(self, client):
        register(client)
        response = _add(client, amount="-50")
        assert b"positive" in response.data.lower()

    def test_add_missing_date_shows_error(self, client):
        register(client)
        response = _add(client, date="")
        assert b"Date is required" in response.data

    def test_add_form_preloads_today(self, client):
        register(client)
        response = client.get("/expenses/add")
        assert b"2026-06-14" in response.data

    def test_add_get_shows_category_dropdown(self, client):
        register(client)
        response = client.get("/expenses/add")
        for cat in [b"Food", b"Transport", b"Health", b"Other"]:
            assert cat in response.data


# ── Edit expense ──────────────────────────────────────────────────────────────

class TestEditExpense:
    def _get_expense_id(self, client):
        """Add an expense and scrape its edit link id from the dashboard."""
        _add(client)
        response = client.get("/dashboard")
        # The edit URL is /expenses/<id>/edit — find the first occurrence
        import re
        match = re.search(rb"/expenses/(\d+)/edit", response.data)
        assert match, "No expense edit link found on dashboard"
        return int(match.group(1))

    def test_edit_success_updates_record(self, client):
        register(client)
        exp_id = self._get_expense_id(client)
        response = client.post(
            f"/expenses/{exp_id}/edit",
            data={"title": "Latte", "amount": "150", "category": "Food",
                  "date": "2026-06-14", "note": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Latte" in response.data

    def test_edit_missing_title_shows_error(self, client):
        register(client)
        exp_id = self._get_expense_id(client)
        response = client.post(
            f"/expenses/{exp_id}/edit",
            data={"title": "", "amount": "150", "category": "Food",
                  "date": "2026-06-14", "note": ""},
            follow_redirects=True,
        )
        assert b"Title is required" in response.data

    def test_edit_prefills_existing_values(self, client):
        register(client)
        exp_id = self._get_expense_id(client)
        response = client.get(f"/expenses/{exp_id}/edit")
        assert b"Coffee" in response.data
        assert b"120" in response.data

    def test_edit_another_users_expense_redirects(self, client):
        """User A cannot edit User B's expense — redirected to dashboard."""
        register(client, name="Alice", email="alice@example.com")
        _add(client)
        exp_id = self._get_expense_id(client)
        logout(client)

        register(client, name="Bob", email="bob@example.com")
        response = client.post(
            f"/expenses/{exp_id}/edit",
            data={"title": "Hacked", "amount": "1", "category": "Other",
                  "date": "2026-06-14", "note": ""},
            follow_redirects=True,
        )
        # Should redirect to Bob's dashboard without modifying Alice's expense
        assert b"Hacked" not in response.data or b"Coffee" in response.data

    def test_edit_requires_login(self, client):
        response = client.get("/expenses/999/edit", follow_redirects=True)
        assert b"Sign in" in response.data or b"login" in response.data.lower()


# ── Delete expense ────────────────────────────────────────────────────────────

class TestDeleteExpense:
    def _add_and_get_id(self, client):
        _add(client)
        response = client.get("/dashboard")
        import re
        match = re.search(rb"/expenses/(\d+)/edit", response.data)
        assert match
        return int(match.group(1))

    def test_delete_removes_expense_from_dashboard(self, client):
        register(client)
        exp_id = self._add_and_get_id(client)
        response = client.post(
            f"/expenses/{exp_id}/delete",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Coffee" not in response.data

    def test_delete_another_users_expense_has_no_effect(self, client):
        """User B's delete request on User A's expense is silently ignored."""
        register(client, name="Alice", email="alice@example.com")
        exp_id = self._add_and_get_id(client)
        logout(client)

        register(client, name="Bob", email="bob@example.com")
        client.post(f"/expenses/{exp_id}/delete", follow_redirects=True)
        logout(client)

        # Alice's expense should still exist
        login(client, email="alice@example.com")
        response = client.get("/dashboard")
        assert b"Coffee" in response.data

    def test_delete_requires_login(self, client):
        response = client.post("/expenses/999/delete", follow_redirects=True)
        assert b"Sign in" in response.data or b"login" in response.data.lower()
