import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flasgger import Swagger
from database.db import get_db, init_db
from api_routes import api

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# JSON API Blueprint (all routes under /api/)
app.register_blueprint(api)

# Swagger UI at /apidocs/
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: rule.rule.startswith("/api/"),
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Spendly API",
        "description": (
            "REST API for Spendly — personal expense tracker.\n\n"
            "**How to authenticate:** call `POST /api/auth/login` first; "
            "the session cookie is stored in your browser and sent automatically "
            "with every subsequent request."
        ),
        "version": "1.0.0",
    },
    "host": "127.0.0.1:5001",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {"name": "Auth",      "description": "Register, login, logout"},
        {"name": "Dashboard", "description": "Spending summary"},
        {"name": "Expenses",  "description": "Create, read, update, delete expenses"},
        {"name": "Profile",   "description": "User profile and password"},
    ],
}
Swagger(app, config=swagger_config, template=swagger_template)

# Initialise tables on startup
with app.app_context():
    init_db()


# ------------------------------------------------------------------ #
# Public routes                                                        #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Basic validation
        if not name or not email or not password:
            error = "All fields are required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            db = get_db()
            existing = db.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()

            if existing:
                error = "An account with that email already exists."
            else:
                hashed = generate_password_hash(password)
                db.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed),
                )
                db.commit()
                user = db.execute(
                    "SELECT id, name FROM users WHERE email = ?", (email,)
                ).fetchone()
                db.close()

                session["user_id"]   = user["id"]
                session["user_name"] = user["name"]
                return redirect(url_for("dashboard"))

            db.close()

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            error = "Email and password are required."
        else:
            db   = get_db()
            user = db.execute(
                "SELECT id, name, password FROM users WHERE email = ?", (email,)
            ).fetchone()
            db.close()

            if user is None or not check_password_hash(user["password"], password):
                error = "Invalid email or password."
            else:
                session["user_id"]   = user["id"]
                session["user_name"] = user["name"]
                return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Protected routes (login required)                                   #
# ------------------------------------------------------------------ #

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = get_db()

    # Total spent this month
    month_total = db.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
          AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """, (user_id,)).fetchone()[0]

    # All-time total
    all_total = db.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    # Total number of transactions
    tx_count = db.execute("""
        SELECT COUNT(*) FROM expenses WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    # Spending by category (all-time, sorted desc)
    categories = db.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """, (user_id,)).fetchall()

    # Recent 5 expenses
    recent = db.execute("""
        SELECT id, title, amount, category, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT 5
    """, (user_id,)).fetchall()

    db.close()

    # For category bar widths (% relative to largest category)
    max_cat = categories[0]["total"] if categories else 1

    return render_template("dashboard.html",
        name        = session["user_name"],
        month_total = month_total,
        all_total   = all_total,
        tx_count    = tx_count,
        categories  = categories,
        recent      = recent,
        max_cat     = max_cat,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = get_db()
    user = db.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    # Stats for the summary strip
    stats = db.execute("""
        SELECT COUNT(*) AS tx_count,
               COALESCE(SUM(amount), 0) AS total_spent
        FROM expenses WHERE user_id = ?
    """, (user_id,)).fetchone()

    info_error = info_success = pw_error = pw_success = None

    if request.method == "POST":
        action = request.form.get("action")

        # ── Update name / email ──────────────────────────────────────
        if action == "update_info":
            name = request.form.get("name", "").strip()

            if not name:
                info_error = "Name is required."
            else:
                db.execute(
                    "UPDATE users SET name = ? WHERE id = ?",
                    (name, user_id)
                )
                db.commit()
                session["user_name"] = name   # keep navbar in sync
                info_success = "Profile updated successfully."
                # Refresh user row
                user = db.execute(
                    "SELECT id, name, email, created_at FROM users WHERE id = ?",
                    (user_id,)
                ).fetchone()

        # ── Change password ──────────────────────────────────────────
        elif action == "change_password":
            current  = request.form.get("current_password", "")
            new_pw   = request.form.get("new_password", "")
            confirm  = request.form.get("confirm_password", "")

            stored = db.execute(
                "SELECT password FROM users WHERE id = ?", (user_id,)
            ).fetchone()["password"]

            if not check_password_hash(stored, current):
                pw_error = "Current password is incorrect."
            elif len(new_pw) < 8:
                pw_error = "New password must be at least 8 characters."
            elif new_pw != confirm:
                pw_error = "Passwords do not match."
            else:
                db.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (generate_password_hash(new_pw), user_id)
                )
                db.commit()
                pw_success = "Password changed successfully."

    db.close()
    return render_template("profile.html",
        user         = user,
        stats        = stats,
        info_error   = info_error,
        info_success = info_success,
        pw_error     = pw_error,
        pw_success   = pw_success,
    )


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("login"))

    CATEGORIES = ["Food", "Transport", "Entertainment",
                  "Utilities", "Health", "Education", "Subscriptions", "SchoolFees", "Travel", "Other"]
    error = None

    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        amount   = request.form.get("amount", "").strip()
        category = request.form.get("category", "Other")
        date     = request.form.get("date", "").strip()
        note     = request.form.get("note", "").strip()

        # Validation
        if not title:
            error = "Title is required."
        elif not amount:
            error = "Amount is required."
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                error = "Amount must be a positive number."

        if not date:
            error = "Date is required."

        if not error:
            db = get_db()
            db.execute(
                """INSERT INTO expenses (user_id, title, amount, category, date, note)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (session["user_id"], title, amount, category, date, note or None),
            )
            db.commit()
            db.close()
            return redirect(url_for("dashboard"))

    from datetime import date as _date
    return render_template("add_expense.html",
                           categories=CATEGORIES,
                           error=error,
                           today=_date.today().isoformat())


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = get_db()

    # Fetch the expense — must belong to this user
    expense = db.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (id, user_id)
    ).fetchone()

    if expense is None:
        db.close()
        return redirect(url_for("dashboard"))   # not found or not theirs

    CATEGORIES = ["Food", "Transport", "Entertainment",
                  "Utilities", "Health", "Education", "Subscriptions", "SchoolFees", "Travel", "Other"]
    error = None

    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        amount   = request.form.get("amount", "").strip()
        category = request.form.get("category", "Other")
        date     = request.form.get("date", "").strip()
        note     = request.form.get("note", "").strip()

        if not title:
            error = "Title is required."
        elif not amount:
            error = "Amount is required."
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                error = "Amount must be a positive number."

        if not date:
            error = "Date is required."

        if not error:
            db.execute(
                """UPDATE expenses
                   SET title = ?, amount = ?, category = ?, date = ?, note = ?
                   WHERE id = ? AND user_id = ?""",
                (title, amount, category, date, note or None, id, user_id),
            )
            db.commit()
            db.close()
            return redirect(url_for("dashboard"))

    db.close()
    return render_template("edit_expense.html",
                           expense=expense,
                           categories=CATEGORIES,
                           error=error)


@app.route("/expenses/<int:id>/delete", methods=["POST"])
def delete_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    db.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (id, session["user_id"])
    )
    db.commit()
    db.close()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
