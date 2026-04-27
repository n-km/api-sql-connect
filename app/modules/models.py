"""
Data Models

This module defines the Pydantic schemas used for data validation 
in the API requests and responses.
"""

from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    """Schema for login and registration."""
    email: EmailStr
    password: str

class UpdateProfileRequest(BaseModel):
    """Schema for updating email and username."""
    currentEmail: EmailStr
    newEmail: EmailStr
    newUsername: str

class ChangePasswordRequest(BaseModel):
    """Schema for changing the user password."""
    email: EmailStr
    currentPassword: str
    newPassword: str