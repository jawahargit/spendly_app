# Spendly — Complete Project Documentation

> A personal expense tracker built with Python, Flask, SQLite, and vanilla CSS.  
> This document covers everything from project setup to architecture, file-by-file explanations, and data flow.
> https://youtu.be/YjLF6jTyAVk?si=NPzIUxXdosuq6h1K

---

## Table of Contents

1. [What the App Does](#1-what-the-app-does)
2. [Tech Stack Overview](#2-tech-stack-overview)
3. [Starting the Project in VS Code (From Scratch)](#3-starting-the-project-in-vs-code-from-scratch)
4. [Step-by-Step Build Guide](#4-step-by-step-build-guide)
5. [Project Structure](#5-project-structure)
6. [File-by-File Explanation](#6-file-by-file-explanation)
7. [Database Schema](#7-database-schema)
8. [Architecture Diagram](#8-architecture-diagram)
9. [Request–Response Flow](#9-requestresponse-flow)
10. [Authentication Flow](#10-authentication-flow)
11. [Route Map](#11-route-map)
12. [How Each Module Powers the App](#12-how-each-module-powers-the-app)

---

## 1. What the App Does

**Spendly** is a personal finance web app where users can:

- ✅ Register and log in securely
- ✅ Add, edit, and delete expenses
- ✅ View a dashboard with spending stats (this month, all time, transaction count)
- ✅ See spending broken down by category in a doughnut chart
- ✅ View their 5 most recent transactions
- ✅ Manage their profile (update name, change password)

---

## 2. Tech Stack Overview

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3 | Backend logic |
| Web Framework | Flask 3.1 | Routing, templating, sessions |
| Database | SQLite 3 | Persistent data storage |
| DB Driver | `sqlite3` (stdlib) | Python ↔ SQLite |
| Password Hashing | Werkzeug (PBKDF2) | Secure password storage |
| Templating | Jinja2 (via Flask) | Dynamic HTML rendering |
| CSS | Plain CSS + custom properties | Styling and layout |
| Fonts | Google Fonts (DM Serif Display, DM Sans) | Typography |
| Chart | Chart.js 4.4 (CDN) | Doughnut chart on dashboard |
| Testing | pytest + pytest-flask | Automated tests |

---

## 3. Starting the Project in VS Code (From Scratch)

### Prerequisites
- Python 3.10+ installed
- VS Code installed
- Python extension for VS Code (ms-python.python)

### Step 1 — Open VS Code and create the project folder

```
File → Open Folder → Create New Folder → "expense-tracker" → Open
```

Or from the terminal:

```bash
mkdir expense-tracker
cd expense-tracker
code .
```

### Step 2 — Open the integrated terminal

```
Terminal → New Terminal   (or  Ctrl + `)
```

### Step 3 — Create a Python virtual environment

```bash
python3 -m venv venv
```

This creates an isolated Python environment inside `venv/` so packages you install don't affect your system Python.

### Step 4 — Activate the virtual environment

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 5 — Select the interpreter in VS Code

```
Ctrl + Shift + P  →  "Python: Select Interpreter"  →  choose  ./venv/bin/python
```

### Step 6 — Create `requirements.txt`

Create a file named `requirements.txt` in the project root:

```
flask==3.1.3
werkzeug==3.1.6
pytest==8.3.5
pytest-flask==1.3.0
```

### Step 7 — Install dependencies

```bash
venv/bin/pip install -r requirements.txt
```

### Step 8 — Create the folder structure

```bash
mkdir -p database static/css static/js templates
touch app.py
touch database/__init__.py database/db.py
touch static/css/style.css static/js/main.js
```

### Step 9 — Run the app

```bash
venv/bin/python app.py
```

Open your browser at: **http://127.0.0.1:5001**

---

## 4. Step-by-Step Build Guide

The project was built incrementally in the following steps:

---

### Step 1 — Database Setup (`database/db.py`)

**Goal:** Set up SQLite with two tables — `users` and `expenses`.

Three functions were written:

```
get_db()   → Opens a SQLite connection with row_factory and foreign keys
init_db()  → Creates users and expenses tables (CREATE TABLE IF NOT EXISTS)
seed_db()  → Inserts sample users and expenses for development
```

Run once to initialise:

```bash
venv/bin/python database/db.py
```

This creates `database/spendly.db` — the live database file.

---

### Step 2 — Landing, Login, Register pages (HTML only)

**Goal:** Build the visual shell — navbar, landing page, auth forms — before any backend logic.

- `templates/base.html` — shared layout (navbar + footer)
- `templates/landing.html` — marketing home page
- `templates/login.html` — sign-in form
- `templates/register.html` — sign-up form
- `static/css/style.css` — full design system

Flask routes were added as GET-only at this stage — just rendering the templates.

---

### Step 3 — Authentication Backend (Login, Register, Logout)

**Goal:** Make the auth forms actually work — validate input, hash passwords, manage sessions.

What was implemented in `app.py`:

- `POST /register` — validates name/email/password, hashes password with Werkzeug, inserts user, starts session
- `POST /login` — checks email + password hash, starts session on success
- `GET /logout` — clears the session, redirects to landing
- Flask `session` stores `user_id` and `user_name` across requests
- `base.html` navbar updated: shows Dashboard + Profile + Log out when logged in

---

### Step 4 — Dashboard

**Goal:** Build the main screen users see after logging in.

The `/dashboard` route queries the database for:

- Total spent this month (SQL: `strftime('%Y-%m', date)`)
- All-time total
- Transaction count
- Top 5 spending categories (GROUP BY category)
- 5 most recent expenses

Then renders `dashboard.html` with:
- 3 stat cards
- Doughnut chart (Chart.js via CDN)
- Recent expenses list with Edit / Delete buttons

---

### Step 5 — Add Expense

**Goal:** Let users log a new transaction.

- `GET /expenses/add` — renders `add_expense.html` with today's date pre-filled
- `POST /expenses/add` — validates title/amount/date, inserts into `expenses` table, redirects to dashboard
- Category is a `<select>` dropdown: Food, Transport, Entertainment, Utilities, Health, Education, Other

---

### Step 6 — Profile Page

**Goal:** Let users update their name and change their password.

- `GET /profile` — shows user info + stats (member since, transactions, total spent)
- `POST /profile` with `action=update_info` — updates name only (email is read-only)
- `POST /profile` with `action=change_password` — verifies current password, validates new password, saves hash

A hidden `<input name="action">` field in each form tells the backend which action to take.

---

### Step 7 — Edit Expense

**Goal:** Let users update an existing expense.

- `GET /expenses/<id>/edit` — fetches the expense from DB, renders `edit_expense.html` with pre-filled values
- `POST /expenses/<id>/edit` — validates and runs `UPDATE expenses SET ... WHERE id = ? AND user_id = ?`
- The `AND user_id = ?` clause ensures users can only edit their own expenses

---

### Step 8 — Delete Expense

**Goal:** Let users remove an expense.

- `POST /expenses/<id>/delete` — runs `DELETE FROM expenses WHERE id = ? AND user_id = ?`
- Uses `POST` (not `GET`) so a browser prefetch or accidental click can't delete data
- Dashboard shows a `<form>` with a submit button styled as a link, with `onsubmit="return confirm(...)"` for a browser confirmation dialog

---

### Step 9 — Doughnut Chart

**Goal:** Replace the CSS progress bars in the dashboard with a visual chart.

- Chart.js 4.4 loaded from jsDelivr CDN (no npm/install needed)
- Category labels and totals are passed from Flask to Jinja2, then serialised into a `<script type="application/json">` block
- JavaScript reads that JSON and renders a doughnut chart
- A custom legend below the chart shows dots coloured to match each segment

---

## 5. Project Structure

```
expense-tracker/
│
├── app.py                    ← All backend routes and logic
├── requirements.txt          ← Python package dependencies
│
├── database/
│   ├── __init__.py           ← Makes database/ a Python package
│   ├── db.py                 ← get_db(), init_db(), seed_db()
│   └── spendly.db            ← SQLite database file (auto-created)
│
├── templates/
│   ├── base.html             ← Master layout (navbar, footer, CSS/JS links)
│   ├── landing.html          ← Public home / marketing page
│   ├── login.html            ← Sign-in form
│   ├── register.html         ← Sign-up form
│   ├── dashboard.html        ← Main app screen (stats + chart + expenses)
│   ├── add_expense.html      ← Add new transaction form
│   ├── edit_expense.html     ← Edit existing transaction form
│   └── profile.html          ← User info + change password
│
├── static/
│   ├── css/
│   │   └── style.css         ← Complete stylesheet (design system + every page)
│   └── js/
│       └── main.js           ← Frontend JavaScript (chart logic is inline)
│
└── venv/                     ← Python virtual environment (never edit)
```

---

## 6. File-by-File Explanation

---

### `app.py` — The Brain

The single file that runs the entire backend.

```
Flask app
│
├── app.secret_key            → Signs session cookies so they can't be tampered with
├── init_db() on startup      → Ensures tables exist every time the server starts
│
├── Public routes (no login needed)
│   ├── GET  /                → Landing page
│   ├── GET  /register        → Show register form
│   ├── POST /register        → Validate → hash password → insert user → start session
│   ├── GET  /login           → Show login form
│   ├── POST /login           → Check credentials → start session
│   └── GET  /logout          → Clear session → redirect to /
│
└── Protected routes (redirect to /login if no session)
    ├── GET  /dashboard             → Fetch stats + categories + recent → render chart
    ├── GET  /profile               → Show user info + stats
    ├── POST /profile               → Update name  OR  change password (via action field)
    ├── GET  /expenses/add          → Show empty form
    ├── POST /expenses/add          → Validate → INSERT → redirect to dashboard
    ├── GET  /expenses/<id>/edit    → Fetch expense → show pre-filled form
    ├── POST /expenses/<id>/edit    → Validate → UPDATE → redirect to dashboard
    └── POST /expenses/<id>/delete  → DELETE → redirect to dashboard
```

**Key libraries used in app.py:**

| Import | Used for |
|--------|---------|
| `Flask` | App instance, routing, `render_template`, `redirect`, `url_for` |
| `request` | Reading form data (`request.form.get(...)`) |
| `session` | Storing `user_id` and `user_name` across requests |
| `generate_password_hash` | Hashing plain-text password before saving |
| `check_password_hash` | Verifying a plain-text password against a stored hash |
| `get_db`, `init_db` | From our own `database/db.py` |

---

### `database/db.py` — The Data Layer

Handles all direct communication with the SQLite database.

#### `get_db()`

```python
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # rows act like dicts: row["name"]
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
```

- Opens a connection to `spendly.db`
- `row_factory = sqlite3.Row` means you can access columns by name instead of index
- `PRAGMA foreign_keys = ON` enforces that `expenses.user_id` must exist in `users.id`

#### `init_db()`

```python
def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (...);
        CREATE TABLE IF NOT EXISTS expenses (...);
    """)
```

- Creates both tables if they don't already exist
- Called automatically every time `app.py` starts

#### `seed_db()`

```python
def seed_db():
    # Inserts 2 sample users and 7 sample expenses
    # Skips if data already exists
```

- Populates the database with realistic-looking sample data
- Safe to call multiple times — checks `COUNT(*)` before inserting

---

### `database/__init__.py` — Package Marker

Empty file. Its only job is to tell Python that `database/` is a package, which allows:

```python
from database.db import get_db, init_db
```

---

### `database/spendly.db` — The Database File

- Auto-created by `init_db()` on first run
- A single `.db` file that stores all users and expenses
- Can be opened and inspected with [DB Browser for SQLite](https://sqlitebrowser.org/)
- **Never commit this to git** — it contains real user data

---

### `templates/base.html` — The Master Layout

Every other template extends this file:

```html
{% extends "base.html" %}
{% block content %} ... {% endblock %}
```

It provides:
- `<head>` with meta tags, Google Fonts, and `style.css` link
- Sticky navbar — shows Sign in / Get started when logged out, Dashboard / Profile / Log out when logged in
- `{% block content %}` — where each page inserts its body
- Footer
- `main.js` script tag
- `{% block scripts %}` — where pages like dashboard inject Chart.js

The navbar uses Jinja2's `session` object directly:

```html
{% if session.user_id %}
    👋 {{ session.user_name }}  |  Dashboard  |  Profile  |  Log out
{% else %}
    Sign in  |  Get started
{% endif %}
```

---

### `templates/landing.html` — Home Page

The public marketing page. Contains:
- Hero section with headline, subtitle, and CTA buttons
- Mock spending card (static visual)
- Features section (3 cards)
- Call-to-action banner

No dynamic data — purely static HTML rendered by Flask.

---

### `templates/login.html` / `templates/register.html` — Auth Forms

Both forms:
- `POST` their data to the same route (e.g. `action="/login"`)
- Display `{{ error }}` if the backend sets it (wrong password, duplicate email, etc.)
- Redirect to dashboard on success

---

### `templates/dashboard.html` — Main App Screen

The most data-rich page. Receives from Flask:

| Variable | Type | Content |
|----------|------|---------|
| `name` | string | Logged-in user's name |
| `month_total` | float | Sum of expenses this calendar month |
| `all_total` | float | Sum of all expenses ever |
| `tx_count` | int | Total number of transactions |
| `categories` | list of Rows | `[{category, total}, ...]` sorted by total desc |
| `recent` | list of Rows | Last 5 expenses |
| `max_cat` | float | Largest category total (for bar scaling) |

The chart data is passed to JavaScript via a JSON script block:

```html
<script id="chartData" type="application/json">
{
    "labels": {{ categories | map(attribute='category') | list | tojson }},
    "values": {{ categories | map(attribute='total')    | list | tojson }}
}
</script>
```

JavaScript reads this, creates the Chart.js doughnut, and colours the legend dots.

---

### `templates/add_expense.html` / `templates/edit_expense.html` — Expense Forms

Both have the same fields:

| Field | Input type | Validation |
|-------|-----------|------------|
| Title | text | Required |
| Amount | number (step 0.01, min 0.01) | Required, must be > 0 |
| Date | date | Required, defaults to today |
| Category | select dropdown | One of 7 fixed options |
| Note | textarea | Optional |

**Add** starts with empty/today values.  
**Edit** pre-fills values from the existing database row.  
If validation fails, both forms **re-render with the user's input preserved** (no data loss).

---

### `templates/profile.html` — User Profile

Two independent forms on the same page, distinguished by a hidden field:

```html
<!-- Form 1 -->
<input type="hidden" name="action" value="update_info">
<!-- fields: name (editable), email (readonly) -->

<!-- Form 2 -->
<input type="hidden" name="action" value="change_password">
<!-- fields: current_password, new_password, confirm_password -->
```

The backend reads `request.form.get("action")` to know which form was submitted.

Email is `readonly` — it's displayed but cannot be changed (enforced in both HTML and backend).

---

### `static/css/style.css` — The Design System

One file styles the entire app. Organised into sections:

```
Variables      → CSS custom properties (colors, fonts, radii)
Reset          → box-sizing, margin/padding reset
Navbar         → sticky top bar, brand, links
Hero           → landing page two-column layout
Mock card      → the static spending preview on landing
Buttons        → .btn-primary, .btn-ghost, .btn-submit
Features       → 3-column feature cards on landing
CTA            → call-to-action section
Auth pages     → .auth-section, .auth-card, .form-input, .auth-error, .auth-success
Form extras    → .form-row (2-col), .form-select, .form-textarea
Dashboard      → .dash-wrap, .stat-grid, .stat-card, .dash-grid, .dash-card
Category chart → .chart-wrap, .chart-legend, .legend-row, .legend-dot
Expense list   → .expense-list, .expense-row, .expense-actions, .action-link
Footer         → dark footer strip
Responsive     → media queries for 900px and 600px breakpoints
```

**Key design tokens:**

```css
:root {
    --ink:          #0f0f0f;   /* primary text */
    --accent:       #1a472a;   /* green — primary brand color */
    --accent-2:     #c17f24;   /* gold — secondary accent */
    --danger:       #c0392b;   /* red — errors, delete */
    --paper:        #f7f6f3;   /* page background */
    --paper-card:   #ffffff;   /* card background */
    --border:       #e4e1da;   /* dividers */

    --font-display: 'DM Serif Display', Georgia, serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
}
```

---

### `static/js/main.js` — Frontend JavaScript

Currently a placeholder. The Chart.js chart logic lives inline in `dashboard.html` inside a `{% block scripts %}` block.

Future JavaScript features (form validation, animations) would go here.

---

### `requirements.txt` — Dependencies

```
flask==3.1.3        ← Web framework
werkzeug==3.1.6     ← Password hashing + WSGI utilities (Flask depends on this)
pytest==8.3.5       ← Test runner
pytest-flask==1.3.0 ← Flask test client helpers
```

Install with:
```bash
venv/bin/pip install -r requirements.txt
```

---

## 7. Database Schema

```
┌─────────────────────────────────────────────┐
│                   users                      │
├──────────────┬───────────────────────────────┤
│ id           │ INTEGER  PK AUTOINCREMENT      │
│ name         │ TEXT     NOT NULL              │
│ email        │ TEXT     NOT NULL UNIQUE       │
│ password     │ TEXT     NOT NULL  (hashed)    │
│ created_at   │ TEXT     DEFAULT datetime('now')│
└──────────────┴───────────────────────────────┘
          │
          │ one user → many expenses
          │ (ON DELETE CASCADE)
          ▼
┌─────────────────────────────────────────────┐
│                  expenses                    │
├──────────────┬───────────────────────────────┤
│ id           │ INTEGER  PK AUTOINCREMENT      │
│ user_id      │ INTEGER  FK → users.id         │
│ title        │ TEXT     NOT NULL              │
│ amount       │ REAL     NOT NULL  CHECK > 0   │
│ category     │ TEXT     DEFAULT 'Other'       │
│ date         │ TEXT     DEFAULT date('now')   │
│ note         │ TEXT     (nullable)            │
│ created_at   │ TEXT     DEFAULT datetime('now')│
└──────────────┴───────────────────────────────┘
```

**Relationships:**
- One `user` has many `expenses`
- `expenses.user_id` is a foreign key to `users.id`
- Deleting a user cascades and deletes all their expenses

---

## 8. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER                                 │
│                                                                 │
│   HTML pages rendered by Jinja2                                 │
│   CSS from static/css/style.css                                 │
│   Chart.js loaded from CDN (jsDelivr)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │  HTTP requests (GET / POST)
                         │  Cookies (session)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        app.py  (Flask)                          │
│                                                                 │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────────┐  │
│  │   Routes    │   │   Sessions   │   │  Password Hashing   │  │
│  │             │   │              │   │                     │  │
│  │ GET /       │   │ session[     │   │ generate_password_  │  │
│  │ POST/login  │   │  "user_id"   │   │ hash()              │  │
│  │ POST/reg..  │   │  "user_name" │   │                     │  │
│  │ GET /dash.. │   │ ]            │   │ check_password_     │  │
│  │ POST /exp.. │   │              │   │ hash()              │  │
│  │ ...         │   │  Signed      │   │                     │  │
│  │             │   │  cookie      │   │  Werkzeug PBKDF2    │  │
│  └──────┬──────┘   └──────────────┘   └─────────────────────┘  │
│         │                                                       │
│         │  calls                                                │
│         ▼                                                       │
│  ┌──────────────────────┐    renders    ┌─────────────────────┐ │
│  │    database/db.py    │               │   templates/*.html  │ │
│  │                      │               │                     │ │
│  │  get_db()            │               │  base.html          │ │
│  │  init_db()           │               │  dashboard.html     │ │
│  │  seed_db()           │               │  login.html         │ │
│  │                      │               │  register.html      │ │
│  └──────────┬───────────┘               │  add_expense.html   │ │
│             │                           │  edit_expense.html  │ │
│             │ SQL queries               │  profile.html       │ │
│             ▼                           └─────────────────────┘ │
│  ┌──────────────────────┐                                       │
│  │   spendly.db         │                                       │
│  │   (SQLite file)      │                                       │
│  │                      │                                       │
│  │   TABLE users        │                                       │
│  │   TABLE expenses     │                                       │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Request–Response Flow

### Example: User adds an expense

```
1. User clicks "+ Add expense" on the dashboard
        │
        ▼
2. Browser sends:  GET /expenses/add
        │
        ▼
3. app.py checks:  "user_id" in session?
        │  YES
        ▼
4. app.py calls:   render_template("add_expense.html", categories=[...], today="2026-06-14")
        │
        ▼
5. Jinja2 renders the HTML, injects categories into <select> and today into <input type="date">
        │
        ▼
6. Browser displays the form
        │
   User fills in: Title="Coffee", Amount=120, Category=Food, Date=today
        │
        ▼
7. Browser sends:  POST /expenses/add
                   Body: title=Coffee&amount=120&category=Food&date=2026-06-14&note=
        │
        ▼
8. app.py reads:   request.form.get("title") → "Coffee"
                   request.form.get("amount") → "120" → float(120) → 120.0
                   Validation passes ✅
        │
        ▼
9. app.py calls:   db.execute("INSERT INTO expenses ...")
                   db.commit()
                   db.close()
        │
        ▼
10. app.py returns: redirect(url_for("dashboard"))
        │
        ▼
11. Browser receives: HTTP 302 → Location: /dashboard
        │
        ▼
12. Browser sends:  GET /dashboard
        │
        ▼
13. Dashboard queries DB, fetches updated stats including the new Coffee expense
        │
        ▼
14. User sees the updated dashboard with Coffee in Recent Expenses ✅
```

---

## 10. Authentication Flow

```
REGISTER
────────
User fills form (name, email, password)
        │
        ▼
POST /register
        │
        ├── name/email/password empty?  → re-render with error
        ├── password < 8 chars?         → re-render with error
        ├── email already in DB?        → re-render with error
        │
        ▼
generate_password_hash(password)   ← Werkzeug PBKDF2, random salt
        │
        ▼
INSERT INTO users (name, email, hashed_password)
        │
        ▼
session["user_id"]   = new_user.id
session["user_name"] = new_user.name
        │
        ▼
redirect → /dashboard  ✅


LOGIN
─────
User fills form (email, password)
        │
        ▼
POST /login
        │
        ├── email or password empty?    → re-render with error
        │
        ▼
SELECT * FROM users WHERE email = ?
        │
        ├── user not found?             → "Invalid email or password"
        ├── check_password_hash(stored, input) fails? → same error
        │                               (same message prevents email enumeration)
        ▼
session["user_id"]   = user.id
session["user_name"] = user.name
        │
        ▼
redirect → /dashboard  ✅


LOGOUT
──────
GET /logout
        │
        ▼
session.clear()   ← removes user_id, user_name from cookie
        │
        ▼
redirect → /  (landing page)  ✅


PROTECTED ROUTE GUARD
─────────────────────
Every protected route starts with:

    if "user_id" not in session:
        return redirect(url_for("login"))

If the session cookie is missing, expired, or tampered with → Flask rejects it
and the user is sent to the login page.
```

---

## 11. Route Map

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/` | Public | Landing / marketing page |
| GET | `/register` | Public | Show registration form |
| POST | `/register` | Public | Process registration |
| GET | `/login` | Public | Show login form |
| POST | `/login` | Public | Process login |
| GET | `/logout` | Protected | Clear session, redirect to `/` |
| GET | `/dashboard` | Protected | Main screen — stats, chart, recent expenses |
| GET | `/profile` | Protected | Show profile info + stats |
| POST | `/profile` | Protected | Update name OR change password |
| GET | `/expenses/add` | Protected | Show add expense form |
| POST | `/expenses/add` | Protected | Save new expense |
| GET | `/expenses/<id>/edit` | Protected | Show pre-filled edit form |
| POST | `/expenses/<id>/edit` | Protected | Save updated expense |
| POST | `/expenses/<id>/delete` | Protected | Delete expense |

---

## 12. How Each Module Powers the App

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   requirements.txt                                                  │
│   ── declares Flask, Werkzeug, pytest                               │
│   ── pip reads this to install everything the app needs             │
│                          │                                          │
│                          ▼                                          │
│   app.py  ◄──────────────────────────────────────────────────────┐  │
│   ── Flask creates the app instance                               │  │
│   ── secret_key signs and verifies session cookies                │  │
│   ── @app.route() maps URLs to Python functions                   │  │
│   ── request object reads incoming form data                      │  │
│   ── session dict persists user identity across pages             │  │
│   ── render_template() hands data to Jinja2                       │  │
│   ── redirect() sends browser to another URL                      │  │
│                │                    │                             │  │
│                ▼                    ▼                             │  │
│   database/db.py           templates/*.html                       │  │
│   ── get_db() opens          ── Jinja2 fills {{ variables }}      │  │
│      SQLite connection          into HTML at render time          │  │
│   ── SQL SELECT/INSERT/      ── {% extends "base.html" %}         │  │
│      UPDATE/DELETE              reuses navbar + footer            │  │
│   ── returns results as      ── {% block content %} defines       │  │
│      dict-like Row objects      each page's unique body           │  │
│                │                    │                             │  │
│                ▼                    ▼                             │  │
│   spendly.db               static/css/style.css                   │  │
│   ── stores all users       ── CSS variables define colours,      │  │
│      and expenses              fonts, spacing once                │  │
│   ── SQLite file on disk    ── every element on every page        │  │
│   ── persists between          is styled from this one file       │  │
│      server restarts                │                             │  │
│                                     ▼                             │  │
│                          Chart.js (CDN)                           │  │
│                          ── loaded in dashboard's {% block        │  │
│                             scripts %}                            │  │
│                          ── reads JSON data embedded in           │  │
│                             the HTML by Jinja2                    │  │
│                          ── renders the doughnut chart            │  │
│                             entirely in the browser               │  │
│                                                     │             │  │
│                                                     └─────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference — Running the App

```bash
# 1. Activate virtual environment
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 2. Install dependencies (first time only)
venv/bin/pip install -r requirements.txt

# 3. Seed the database (first time only)
venv/bin/python database/db.py

# 4. Start the server
venv/bin/python app.py

# 5. Open in browser
# http://127.0.0.1:5001

# Sample login credentials (from seed data)
# Email:    nitish@example.com
# Password: password123
```

---

*Documentation generated for Spendly v1.0 — built with Flask + SQLite*
