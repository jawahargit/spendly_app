"""Tests for registration, login, and logout flows."""

from tests.conftest import register, login, logout


# ── Registration ──────────────────────────────────────────────────────────────

class TestRegister:
    def test_register_success_redirects_to_dashboard(self, client):
        response = register(client)
        assert response.status_code == 200
        assert b"Dashboard" in response.data or b"dashboard" in response.data.lower()

    def test_register_sets_session(self, client):
        with client.session_transaction() as pre:
            assert "user_id" not in pre

        register(client)

        with client.session_transaction() as post:
            assert "user_id" in post
            assert post["user_name"] == "Alice"

    def test_register_duplicate_email_shows_error(self, client):
        register(client)
        logout(client)  # must be logged out to hit the register form again
        response = register(client)  # same email again
        assert b"already exists" in response.data

    def test_register_missing_name_shows_error(self, client):
        response = client.post(
            "/register",
            data={"name": "", "email": "x@example.com", "password": "password123"},
            follow_redirects=True,
        )
        assert b"required" in response.data.lower()

    def test_register_missing_email_shows_error(self, client):
        response = client.post(
            "/register",
            data={"name": "Bob", "email": "", "password": "password123"},
            follow_redirects=True,
        )
        assert b"required" in response.data.lower()

    def test_register_short_password_shows_error(self, client):
        response = client.post(
            "/register",
            data={"name": "Bob", "email": "bob@example.com", "password": "short"},
            follow_redirects=True,
        )
        assert b"8 characters" in response.data

    def test_logged_in_user_redirected_away_from_register(self, client):
        register(client)
        response = client.get("/register", follow_redirects=True)
        # Should land on dashboard, not the register form
        assert b"Sign up" not in response.data


# ── Login ─────────────────────────────────────────────────────────────────────

class TestLogin:
    def test_login_success_redirects_to_dashboard(self, client):
        register(client)
        logout(client)
        response = login(client)
        assert response.status_code == 200
        assert b"Dashboard" in response.data or b"dashboard" in response.data.lower()

    def test_login_sets_session(self, client):
        register(client)
        logout(client)
        login(client)
        with client.session_transaction() as sess:
            assert "user_id" in sess

    def test_login_wrong_password_shows_error(self, client):
        register(client)
        logout(client)
        response = client.post(
            "/login",
            data={"email": "alice@example.com", "password": "wrongpassword"},
            follow_redirects=True,
        )
        assert b"Invalid email or password" in response.data

    def test_login_unknown_email_shows_same_error(self, client):
        response = client.post(
            "/login",
            data={"email": "nobody@example.com", "password": "password123"},
            follow_redirects=True,
        )
        # Same message prevents email enumeration
        assert b"Invalid email or password" in response.data

    def test_login_missing_fields_shows_error(self, client):
        response = client.post(
            "/login",
            data={"email": "", "password": ""},
            follow_redirects=True,
        )
        assert b"required" in response.data.lower()

    def test_logged_in_user_redirected_away_from_login(self, client):
        register(client)
        response = client.get("/login", follow_redirects=True)
        assert b"Sign in" not in response.data


# ── Logout ────────────────────────────────────────────────────────────────────

class TestLogout:
    def test_logout_clears_session(self, client):
        register(client)
        with client.session_transaction() as sess:
            assert "user_id" in sess

        logout(client)

        with client.session_transaction() as sess:
            assert "user_id" not in sess

    def test_logout_redirects_to_landing(self, client):
        register(client)
        response = logout(client)
        assert response.status_code == 200
        # Landing page has the brand tagline
        assert b"Spendly" in response.data

    def test_protected_route_after_logout_redirects_to_login(self, client):
        register(client)
        logout(client)
        response = client.get("/dashboard", follow_redirects=True)
        assert b"Sign in" in response.data or b"login" in response.data.lower()
