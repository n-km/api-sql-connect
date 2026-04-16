from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simplified Schema
class UserAuth(BaseModel):
    email: str
    password: str

def get_db_connection():
    # Adjusted path to local directory for testing
    conn = sqlite3.connect("data.db") 
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    return conn

@app.post("/register")
def register_user(user: UserAuth):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, user.password)
        )
        conn.commit()
        return {"status": "success", "message": "Account created successfully"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Email already registered"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@app.post("/login")
def login_user(user: UserAuth):
    conn = get_db_connection()
    cursor = conn.cursor()
    user_data = cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", 
        (user.email, user.password)
    ).fetchone()
    conn.close()

    if user_data:
        return {"status": "success", "message": "Login successful"}
    else:
        return {"status": "error", "message": "Invalid email or password"}

@app.get("/users")
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute("SELECT id, email FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]