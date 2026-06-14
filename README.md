# Spendly — Personal Expense Tracker

A personal finance web app built with **Python / Flask**, **SQLite**, and **vanilla CSS/JS**. Track every rupee, own your finances.

---

## Features

- Register and log in securely (passwords hashed with Werkzeug PBKDF2)
- Add, edit, and delete personal expenses
- Dashboard with this-month total, all-time total, and transaction count
- Spending breakdown by category — doughnut chart (Chart.js)
- Recent transactions list with inline edit / delete
- Profile page — update display name, change password
- Public Terms & Conditions and Privacy Policy pages
- Full automated test suite (42 tests) with per-run HTTP trace log

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Web framework | Flask 3.1 |
| Database | SQLite 3 (via `sqlite3` stdlib) |
| Password hashing | Werkzeug (PBKDF2) |
| Templating | Jinja2 |
| CSS | Plain CSS with custom properties |
| Fonts | Google Fonts — DM Serif Display, DM Sans |
| Chart | Chart.js 4.4 (CDN) |
| Testing | pytest + pytest-flask |

---

## Quick Start

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd expense-tracker

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
venv/bin/pip install -r requirements.txt

# 4. Seed the database with sample data
venv/bin/python database/db.py

# 5. Start the development server
venv/bin/python app.py
```

Open **http://127.0.0.1:5001** in your browser.

**Sample credentials** (from seed data):
- Email: `nitish@example.com`
- Password: `password123`

> **Environment variable:** create a `.env` file in the project root with `SECRET_KEY=your-secret-here` before running.

---

## Running Tests

```bash
# Run all 42 tests (quiet)
venv/bin/pytest

# Verbose with live HTTP trace printed to terminal
venv/bin/pytest -v -s
```

A full HTTP trace log is auto-written to **`tests/test_logs.md`** after every run (previous log is always deleted first). Each entry shows the request payload, HTTP status, page landed on, and any error messages returned.

---

## Project Structure

```
expense-tracker/
├── app.py                  ← All routes and backend logic
├── requirements.txt
├── pytest.ini
│
├── database/
│   ├── db.py               ← get_db(), init_db(), seed_db()
│   └── spendly.db          ← SQLite file (auto-created, not committed)
│
├── templates/
│   ├── base.html           ← Master layout (navbar + footer)
│   ├── landing.html        ← Public marketing page
│   ├── login.html / register.html
│   ├── dashboard.html      ← Stats + chart + recent expenses
│   ├── add_expense.html / edit_expense.html
│   ├── profile.html
│   ├── terms.html          ← Terms & Conditions (public)
│   └── privacy.html        ← Privacy Policy (public)
│
├── static/
│   ├── css/style.css       ← Full design system (CSS custom properties)
│   └── js/main.js
│
├── tests/
│   ├── conftest.py         ← Fixtures, InstrumentedClient, log hooks
│   ├── test_auth.py        ← 16 tests
│   ├── test_expenses.py    ← 17 tests
│   ├── test_dashboard.py   ← 9 tests
│   └── test_logs.md        ← Auto-generated on every test run
│
└── .claude/commands/       ← Project slash commands for Claude Code
    ├── seed.md             ← /seed
    ├── run.md              ← /run
    ├── test.md             ← /test
    └── add-category.md     ← /add-category <name>
```

---

## Route Map

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/` | Public | Landing page |
| GET / POST | `/register` | Public | Register a new account |
| GET / POST | `/login` | Public | Sign in |
| GET | `/logout` | Public | Clear session, redirect to `/` |
| GET | `/terms` | Public | Terms & Conditions |
| GET | `/privacy` | Public | Privacy Policy |
| GET | `/dashboard` | Protected | Stats, chart, recent expenses |
| GET / POST | `/profile` | Protected | Update name or change password |
| GET / POST | `/expenses/add` | Protected | Add a new expense |
| GET / POST | `/expenses/<id>/edit` | Protected | Edit an existing expense |
| POST | `/expenses/<id>/delete` | Protected | Delete an expense |

---

## Project Slash Commands (Claude Code)

When working in this repo with Claude Code, four `/` commands are available:

| Command | What it does |
|---------|-------------|
| `/seed` | Wipes `spendly.db` and reseeds it with sample data |
| `/run` | Seeds DB if needed, then starts the dev server on port 5001 |
| `/test` | Runs `pytest -v` and reports results |
| `/add-category <name>` | Adds a new expense category to both places in `app.py` |

---

## Documentation

- **`PROJECT_DOCS.md`** — full architecture, file-by-file explanation, DB schema, auth flow diagrams, request-response walkthroughs, and test suite details
- **`CLAUDE.md`** — guidance for Claude Code: commands, architecture notes, CSS variables, security notes, testing setup

---

## Security Notes

- `SECRET_KEY` is read from the environment — never hardcoded
- Passwords stored as Werkzeug PBKDF2 hashes, never plain text
- All expense mutations include `AND user_id = ?` — users cannot touch each other's data
- Login returns the same error for unknown email and wrong password (prevents email enumeration)
