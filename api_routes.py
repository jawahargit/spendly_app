from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db

api = Blueprint("api", __name__, url_prefix="/api")

CATEGORIES = [
    "Food", "Transport", "Entertainment", "Utilities", "Health",
    "Education", "Subscriptions", "SchoolFees", "Travel", "Other",
]


def _auth_required():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401
    return None


# ------------------------------------------------------------------ #
# Auth                                                                 #
# ------------------------------------------------------------------ #

@api.route("/auth/register", methods=["POST"])
def api_register():
    """Register a new user account.
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, email, password]
          properties:
            name:
              type: string
              example: Jane Doe
            email:
              type: string
              example: jane@example.com
            password:
              type: string
              example: secret123
    responses:
      201:
        description: Registered successfully
      400:
        description: Validation error
      409:
        description: Email already in use
    """
    data = request.get_json() or {}
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    db = get_db()
    if db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
        db.close()
        return jsonify({"error": "An account with that email already exists."}), 409

    db.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    db.commit()
    user = db.execute("SELECT id, name, email FROM users WHERE email = ?", (email,)).fetchone()
    db.close()

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return jsonify({"message": "Registered successfully.", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}), 201


@api.route("/auth/login", methods=["POST"])
def api_login():
    """Login with email and password.
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
              example: nitish@example.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful — session cookie is set
      400:
        description: Missing fields
      401:
        description: Invalid credentials
    """
    data     = request.get_json() or {}
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    db   = get_db()
    user = db.execute("SELECT id, name, password FROM users WHERE email = ?", (email,)).fetchone()
    db.close()

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password."}), 401

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return jsonify({"message": "Login successful.", "user": {"id": user["id"], "name": user["name"]}}), 200


@api.route("/auth/logout", methods=["POST"])
def api_logout():
    """Logout the current user and clear the session.
    ---
    tags:
      - Auth
    responses:
      200:
        description: Logged out
    """
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200


# ------------------------------------------------------------------ #
# Dashboard                                                            #
# ------------------------------------------------------------------ #

@api.route("/dashboard", methods=["GET"])
def api_dashboard():
    """Get dashboard summary stats for the logged-in user.
    ---
    tags:
      - Dashboard
    responses:
      200:
        description: Summary stats
        schema:
          type: object
          properties:
            month_total:
              type: number
            all_total:
              type: number
            tx_count:
              type: integer
            top_categories:
              type: array
              items:
                type: object
                properties:
                  category:
                    type: string
                  total:
                    type: number
            recent_expenses:
              type: array
              items:
                type: object
      401:
        description: Authentication required
    """
    err = _auth_required()
    if err:
        return err

    user_id = session["user_id"]
    db = get_db()

    month_total = db.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM expenses
        WHERE user_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """, (user_id,)).fetchone()[0]

    all_total = db.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    tx_count = db.execute(
        "SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    categories = db.execute("""
        SELECT category, SUM(amount) AS total FROM expenses
        WHERE user_id = ? GROUP BY category ORDER BY total DESC LIMIT 5
    """, (user_id,)).fetchall()

    recent = db.execute("""
        SELECT id, title, amount, category, date FROM expenses
        WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 5
    """, (user_id,)).fetchall()

    db.close()

    return jsonify({
        "month_total": float(month_total),
        "all_total":   float(all_total),
        "tx_count":    tx_count,
        "top_categories": [
            {"category": r["category"], "total": float(r["total"])} for r in categories
        ],
        "recent_expenses": [
            {"id": r["id"], "title": r["title"], "amount": float(r["amount"]),
             "category": r["category"], "date": r["date"]}
            for r in recent
        ],
    })


# ------------------------------------------------------------------ #
# Expenses — CRUD                                                      #
# ------------------------------------------------------------------ #

@api.route("/expenses", methods=["GET"])
def api_list_expenses():
    """List all expenses for the logged-in user.
    ---
    tags:
      - Expenses
    parameters:
      - in: query
        name: category
        type: string
        description: Filter by category
        enum: [Food, Transport, Entertainment, Utilities, Health, Education, Subscriptions, SchoolFees, Travel, Other]
      - in: query
        name: limit
        type: integer
        default: 50
        description: Max number of results (capped at 200)
    responses:
      200:
        description: List of expenses
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              amount:
                type: number
              category:
                type: string
              date:
                type: string
              note:
                type: string
      401:
        description: Authentication required
    """
    err = _auth_required()
    if err:
        return err

    user_id  = session["user_id"]
    category = request.args.get("category")
    limit    = min(int(request.args.get("limit", 50)), 200)

    db = get_db()
    if category:
        rows = db.execute("""
            SELECT id, title, amount, category, date, note FROM expenses
            WHERE user_id = ? AND category = ? ORDER BY date DESC, id DESC LIMIT ?
        """, (user_id, category, limit)).fetchall()
    else:
        rows = db.execute("""
            SELECT id, title, amount, category, date, note FROM expenses
            WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?
        """, (user_id, limit)).fetchall()
    db.close()

    return jsonify([
        {"id": r["id"], "title": r["title"], "amount": float(r["amount"]),
         "category": r["category"], "date": r["date"], "note": r["note"]}
        for r in rows
    ])


@api.route("/expenses", methods=["POST"])
def api_add_expense():
    """Add a new expense.
    ---
    tags:
      - Expenses
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [title, amount, date]
          properties:
            title:
              type: string
              example: Grocery run
            amount:
              type: number
              example: 45.50
            category:
              type: string
              enum: [Food, Transport, Entertainment, Utilities, Health, Education, Subscriptions, SchoolFees, Travel, Other]
              example: Food
            date:
              type: string
              format: date
              example: "2026-06-15"
            note:
              type: string
              example: Weekly groceries
    responses:
      201:
        description: Expense created
        schema:
          type: object
          properties:
            message:
              type: string
            id:
              type: integer
      400:
        description: Validation error
      401:
        description: Authentication required
    """
    err = _auth_required()
    if err:
        return err

    data     = request.get_json() or {}
    title    = data.get("title", "").strip()
    amount   = data.get("amount")
    category = data.get("category", "Other")
    date     = data.get("date", "").strip()
    note     = data.get("note", "").strip()

    if not title:
        return jsonify({"error": "Title is required."}), 400
    if amount is None:
        return jsonify({"error": "Amount is required."}), 400
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a positive number."}), 400
    if not date:
        return jsonify({"error": "Date is required."}), 400
    if category not in CATEGORIES:
        category = "Other"

    db     = get_db()
    cursor = db.execute(
        "INSERT INTO expenses (user_id, title, amount, category, date, note) VALUES (?, ?, ?, ?, ?, ?)",
        (session["user_id"], title, amount, category, date, note or None),
    )
    db.commit()
    new_id = cursor.lastrowid
    db.close()

    return jsonify({"message": "Expense added.", "id": new_id}), 201


@api.route("/expenses/<int:id>", methods=["GET"])
def api_get_expense(id):
    """Get a single expense by ID.
    ---
    tags:
      - Expenses
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: Expense ID
    responses:
      200:
        description: Expense detail
      401:
        description: Authentication required
      404:
        description: Expense not found
    """
    err = _auth_required()
    if err:
        return err

    db  = get_db()
    row = db.execute(
        "SELECT id, title, amount, category, date, note FROM expenses WHERE id = ? AND user_id = ?",
        (id, session["user_id"]),
    ).fetchone()
    db.close()

    if row is None:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify({
        "id": row["id"], "title": row["title"], "amount": float(row["amount"]),
        "category": row["category"], "date": row["date"], "note": row["note"],
    })


@api.route("/expenses/<int:id>", methods=["PUT"])
def api_edit_expense(id):
    """Update an existing expense (full replace).
    ---
    tags:
      - Expenses
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Updated title
            amount:
              type: number
              example: 99.00
            category:
              type: string
              enum: [Food, Transport, Entertainment, Utilities, Health, Education, Subscriptions, SchoolFees, Travel, Other]
            date:
              type: string
              format: date
              example: "2026-06-15"
            note:
              type: string
    responses:
      200:
        description: Expense updated
      400:
        description: Validation error
      401:
        description: Authentication required
      404:
        description: Expense not found
    """
    err = _auth_required()
    if err:
        return err

    user_id = session["user_id"]
    db      = get_db()
    existing = db.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (id, user_id)
    ).fetchone()

    if existing is None:
        db.close()
        return jsonify({"error": "Expense not found."}), 404

    data     = request.get_json() or {}
    title    = data.get("title",    existing["title"]).strip()
    amount   = data.get("amount",   existing["amount"])
    category = data.get("category", existing["category"])
    date     = data.get("date",     existing["date"]).strip()
    note     = data.get("note",     existing["note"] or "").strip()

    if not title:
        db.close()
        return jsonify({"error": "Title is required."}), 400
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        db.close()
        return jsonify({"error": "Amount must be a positive number."}), 400
    if not date:
        db.close()
        return jsonify({"error": "Date is required."}), 400
    if category not in CATEGORIES:
        category = "Other"

    db.execute(
        "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=? AND user_id=?",
        (title, amount, category, date, note or None, id, user_id),
    )
    db.commit()
    db.close()
    return jsonify({"message": "Expense updated."})


@api.route("/expenses/<int:id>", methods=["DELETE"])
def api_delete_expense(id):
    """Delete an expense by ID.
    ---
    tags:
      - Expenses
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Expense deleted
      401:
        description: Authentication required
      404:
        description: Expense not found
    """
    err = _auth_required()
    if err:
        return err

    user_id = session["user_id"]
    db      = get_db()
    existing = db.execute(
        "SELECT id FROM expenses WHERE id = ? AND user_id = ?", (id, user_id)
    ).fetchone()

    if existing is None:
        db.close()
        return jsonify({"error": "Expense not found."}), 404

    db.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (id, user_id))
    db.commit()
    db.close()
    return jsonify({"message": "Expense deleted."})


# ------------------------------------------------------------------ #
# Profile                                                              #
# ------------------------------------------------------------------ #

@api.route("/profile", methods=["GET"])
def api_get_profile():
    """Get the current user's profile and spending stats.
    ---
    tags:
      - Profile
    responses:
      200:
        description: User profile
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
            created_at:
              type: string
            stats:
              type: object
              properties:
                tx_count:
                  type: integer
                total_spent:
                  type: number
      401:
        description: Authentication required
    """
    err = _auth_required()
    if err:
        return err

    db    = get_db()
    user  = db.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    stats = db.execute("""
        SELECT COUNT(*) AS tx_count, COALESCE(SUM(amount), 0) AS total_spent
        FROM expenses WHERE user_id = ?
    """, (session["user_id"],)).fetchone()
    db.close()

    return jsonify({
        "id": user["id"], "name": user["name"], "email": user["email"],
        "created_at": user["created_at"],
        "stats": {"tx_count": stats["tx_count"], "total_spent": float(stats["total_spent"])},
    })


@api.route("/profile", methods=["PATCH"])
def api_update_profile():
    """Update the current user's display name.
    ---
    tags:
      - Profile
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name]
          properties:
            name:
              type: string
              example: Jane Doe
    responses:
      200:
        description: Name updated
      400:
        description: Validation error
      401:
        description: Authentication required
    """
    err = _auth_required()
    if err:
        return err

    data = request.get_json() or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name is required."}), 400

    db = get_db()
    db.execute("UPDATE users SET name = ? WHERE id = ?", (name, session["user_id"]))
    db.commit()
    db.close()

    session["user_name"] = name
    return jsonify({"message": "Profile updated.", "name": name})


@api.route("/profile/password", methods=["PATCH"])
def api_change_password():
    """Change the current user's password.
    ---
    tags:
      - Profile
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [current_password, new_password]
          properties:
            current_password:
              type: string
              example: oldpassword
            new_password:
              type: string
              example: newpassword123
    responses:
      200:
        description: Password changed
      400:
        description: New password too short
      401:
        description: Current password incorrect or not authenticated
    """
    err = _auth_required()
    if err:
        return err

    data     = request.get_json() or {}
    current  = data.get("current_password", "")
    new_pw   = data.get("new_password", "")

    db     = get_db()
    stored = db.execute(
        "SELECT password FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()["password"]

    if not check_password_hash(stored, current):
        db.close()
        return jsonify({"error": "Current password is incorrect."}), 401
    if len(new_pw) < 8:
        db.close()
        return jsonify({"error": "New password must be at least 8 characters."}), 400

    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (generate_password_hash(new_pw), session["user_id"]),
    )
    db.commit()
    db.close()
    return jsonify({"message": "Password changed successfully."})
