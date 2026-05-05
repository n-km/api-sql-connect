"""
User Management Routes

This module contains all API endpoints related to user authentication,
profile updates, and listing users.
"""

from datetime import datetime
from fastapi import APIRouter
import sqlite3

import fastapi

# Import the database function and models from your other files
# The "." means "look in the same folder as this file"
from .database import get_db_connection
from .models import UserAuth, UpdateProfileRequest, ChangePasswordRequest
from .log import log

# Create the router
router = APIRouter(tags=["User Management"])

@router.post("/register")
def register_user(user: UserAuth):
    """
    Registers a new user.
    
    The username is automatically created using the first part of the email.
    
    Args:
        user (UserAuth): The email and password from the user.
        
    Returns:
        dict: A success message or an error if the email is already used.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, user.password),
        )
        conn.commit()
        log(datetime.now(), "SUCCESS - Registration", user.email)
        return {"status": "success", "message": "Account created successfully"}
    except sqlite3.IntegrityError:
        log(datetime.now(), "ERROR - Registration(Email already registered)", user.email)
        return {"status": "error", "message": "Email already registered"}
    except Exception as e:
        log(datetime.now(), "ERROR - Registration", user.email, str(e))
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@router.post("/login")
def login_user(user: UserAuth):
    """
    Checks if the email and password are correct.

    Args:
        user (UserAuth): The login credentials.

    Returns:
        dict: Success if the data matches, otherwise an error.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    user_data = cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (user.email, user.password),
    ).fetchone()
    conn.close()

    if user_data:
        log(datetime.now(), "Login successful", user.email)
        return {"status": "success", "message": "Login successful", "user_id": user_data[0]}
    return {"status": "error", "message": "Invalid email or password"}

@router.post("/update-profile")
def update_profile(data: UpdateProfileRequest):
    """
    Updates the email for a user.

    Args:
        data (UpdateProfileRequest): The old email and the new information.

    Returns:
        dict: Success message or error.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET email = ? WHERE email = ?",
            (data.newEmail, data.currentEmail),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {"status": "error", "message": "User not found"}

        return {"status": "success", "message": "Profile updated successfully"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Email already registered"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@router.post("/change-password")
def change_password(data: ChangePasswordRequest):
    """
    Changes the password for an existing user.

    Args:
        data (ChangePasswordRequest): Email, old password, and new password.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_data = cursor.execute(
            "SELECT password FROM users WHERE email = ?",
            (data.email,),
        ).fetchone()

        if not user_data:
            return {"status": "error", "message": "User not found"}

        if user_data["password"] != data.currentPassword:
            return {"status": "error", "message": "Current password is incorrect"}

        if data.currentPassword == data.newPassword:
            return {"status": "error", "message": "New password must be different"}

        cursor.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (data.newPassword, data.email),
        )
        conn.commit()

        return {"status": "success", "message": "Password updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@router.get("/users")
def list_users():
    """
    Returns a list of all registered users.
    
    Passwords are not included in the response for security reasons.

    Returns:
        list[dict]: A list of users with their ID, email, and username.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]

@router.get("/plan")
def get_user_plan(email: str):
    """
    Returns the 'plan' of a user based on their email address.
    
    Args:
        email (str): The email address of the user to look up.
    
    Returns:
        dict: A dictionary containing the user's plan, or an error message if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Verwenden Sie ein Parameterized Query, um SQL-Injection zu vermeiden
    user = cursor.execute("SELECT plan FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    
    if user:
        return {"plan": user["plan"]}
    else:
        return {"error": "User not found"}   