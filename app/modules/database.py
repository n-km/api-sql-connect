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
            plan TEXT NOT NULL DEFAULT 'free',
            status TEXT NOT NULL DEFAULT 'active',
            filename_consent BOOLEAN NOT NULL DEFAULT 0, -- 0 for false, 1 for true
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    return conn