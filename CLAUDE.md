# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a personal expense tracker built with Flask, SQLite, and vanilla CSS/JS. Named "Spendly" throughout the UI and database, despite the repo folder being `expense-tracker`.

## Running the App
Use a Python virtual environment: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`. Then run with `venv/bin/python app.py`. If you hit 'externally-managed-environment' errors, always use the venv.

## Commands

```bash
# Install dependencies (first time)
venv/bin/pip install -r requirements.txt

# Run the app (port 5001)
venv/bin/python app.py

# Seed the database with sample data (first time, or after wiping spendly.db)
venv/bin/python database/db.py

# Run tests
venv/bin/pytest

# Run a single test file
venv/bin/pytest tests/test_auth.py -v
```

App runs at **http://127.0.0.1:5001**. Sample seed credentials: `nitish@example.com` / `password123`.

## Architecture

The entire backend lives in a single file, `app.py`. There is no blueprint or service layer — routes call `get_db()` directly, execute SQL inline, and render Jinja2 templates.

**Data layer (`database/db.py`):**
- `get_db()` — opens a SQLite connection with `row_factory = sqlite3.Row` (columns accessible by name) and `PRAGMA foreign_keys = ON`
- `init_db()` — creates `users` and `expenses` tables; called automatically on every `app.py` startup
- `seed_db()` — inserts sample data; safe to call repeatedly (no-ops if data exists)
- Database file: `database/spendly.db` (auto-created, not committed to git)

**Session auth:** Flask's signed cookie session stores `user_id` and `user_name`. Every protected route manually checks `"user_id" not in session` and redirects to `/login` — there is no decorator or middleware for this.

**Profile page multi-form pattern:** Both forms on `/profile` POST to the same route; a hidden `<input name="action">` field (`update_info` or `change_password`) tells the backend which form was submitted.

**Dashboard chart:** Chart.js (loaded from CDN in `dashboard.html`'s `{% block scripts %}`) reads category data embedded as `<script id="chartData" type="application/json">` by Jinja2 — no separate API endpoint.

**Templates:** All pages extend `templates/base.html`. The `{% block scripts %}` extension point is used by `dashboard.html` for Chart.js. The navbar reads `session.user_id` directly in Jinja2.

**CSS:** Single file `static/css/style.css` using CSS custom properties defined in `:root`. Brand colors: `--accent: #1a472a` (green), `--accent-2: #c17f24` (gold), `--danger: #c0392b` (red).

## Fixed categories

Expense categories are hardcoded in `app.py` in both `add_expense` and `edit_expense` routes — update both if adding a new category:
```python
CATEGORIES = ["Food", "Transport", "Entertainment", "Utilities", "Health", "Education", "Other"]
```

## Security notes

- `app.secret_key` is hardcoded as `"spendly-dev-secret-key-change-in-production"` — must be replaced with an environment variable before any real deployment
- All expense mutations (`UPDATE`, `DELETE`) include `AND user_id = ?` to prevent users from touching each other's data
- Login returns the same error message for "user not found" and "wrong password" to prevent email enumeration
