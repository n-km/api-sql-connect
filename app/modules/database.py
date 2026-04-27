import sqlite3

# --- DATABASE LOGIC ---

def get_db_connection():
    """
    Creates a connection to the SQLite database.

    It creates the 'users' table if it does not exist. 
    It also checks if the 'username' column exists and adds it if necessary.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    conn = sqlite3.connect("../data.db")
    conn.row_factory = sqlite3.Row  # This allows accessing data by column name

    # Create the table if it's missing
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            username TEXT
        )
        """
    )

    # Database Migration: Add 'username' column if the database is old
    columns = [row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
    if "username" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN username TEXT")
        conn.commit()

    return conn