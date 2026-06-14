import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "spendly.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL UNIQUE,
                password    TEXT    NOT NULL,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title       TEXT    NOT NULL,
                amount      REAL    NOT NULL CHECK(amount > 0),
                category    TEXT    NOT NULL DEFAULT 'Other',
                date        TEXT    NOT NULL DEFAULT (date('now')),
                note        TEXT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)
    conn.close()
    print("✅ Tables created.")


def seed_db():
    """Insert sample data for development (skips if data already exists)."""
    conn = get_db()
    with conn:
        # Check if already seeded
        existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if existing:
            print("ℹ️  Database already has data — skipping seed.")
            conn.close()
            return

        # Sample users (passwords are plain-text for now; hashing comes later)
        conn.execute("""
            INSERT INTO users (name, email, password) VALUES
            ('Nitish Kumar',  'nitish@example.com', 'password123'),
            ('Priya Sharma',  'priya@example.com',  'password123')
        """)

        # Sample expenses for user 1 (Nitish)
        conn.executemany("""
            INSERT INTO expenses (user_id, title, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, 'Groceries',       1200.00, 'Food',          '2026-05-20', 'Big Bazaar'),
            (1, 'Metro card',       500.00, 'Transport',     '2026-05-19', 'Monthly recharge'),
            (1, 'Netflix',          649.00, 'Entertainment', '2026-05-18', 'Monthly subscription'),
            (1, 'Electricity bill', 980.00, 'Utilities',     '2026-05-15', None),
            (1, 'Lunch',            220.00, 'Food',          '2026-05-22', 'Office canteen'),
            (2, 'Gym membership',  1500.00, 'Health',        '2026-05-01', 'Monthly fee'),
            (2, 'Books',            850.00, 'Education',     '2026-05-10', 'Python textbook'),
        ])

    conn.close()
    print("✅ Sample data seeded.")


if __name__ == "__main__":
    init_db()
    seed_db()
