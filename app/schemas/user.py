from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, SecretStr
from app.common.enums import Language


# =======================
# Base Schema for Users
# =======================
class UserBase(BaseModel):
    """
    Base schema for user-related data.
    Contains common fields that are shared among other user schemas.
    """
    model_config = ConfigDict(from_attributes=True,
                              extra='ignore')


# =======================
# User Login Schema
# =======================
class UserLogin(UserBase):
    """
    Schema for user login.
    Requires phone number and password for authentication.
    """
    phone_number: str = Field(
        ...,
        min_length=9, max_length=13,
        pattern=r'^\+998\d{9}$',
        description="Uzbekistan phone number in format: +998901234567",
        json_schema_extra={
            "examples": ["+998901234567"],
            "error_messages": {
                "pattern": "Phone number must be in format: +998901234567"
            }
        },
        alias="username"
    )

    password: str = Field(
        ...,
        min_length=6, max_length=255,
        description="User password",
        json_schema_extra={
            "examples": ["Password123"],
            "error_messages": {
                "minLength": "Password must be at least 6 characters long"
            }
        }
    )


# =======================
# User Creation Schema
# =======================
class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Inherits fullname from UserBase and adds additional required fields.
    """
    fullname: str = Field(
        ...,
        min_length=3, max_length=255,
        pattern=r'^[a-zA-Z\s\'-]+$',
        description='Fullname must contain only letters, spaces, hyphens, and apostrophes',
        json_schema_extra={
            "examples": ["John Doe"],
            "error_messages": {
                "pattern": "Fullname must contain only letters, spaces, hyphens, and apostrophes"
            }
        }
    )

    phone_number: str = Field(
        ...,
        min_length=9, max_length=13,
        pattern=r'^\+998\d{9}$',
        description="Uzbekistan phone number in format: +998901234567",
        json_schema_extra={
            "examples": ["+998901234567"],
            "error_messages": {
                "pattern": "Phone number must be in format: +998901234567"
            }
        }
    )

    password: str = Field(
        ...,
        min_length=6, max_length=255,
        description="User password",
        json_schema_extra={
            "examples": ["Password123"],
            "error_messages": {
                "minLength": "Password must be at least 6 characters long"
            }
        }
    )

    tg_id: Optional[str] = Field(
        None,
        min_length=5, max_length=255,
        description="Telegram id number",
        pattern=r'^\d{8, 12}$',
        json_schema_extra={
            "examples": ["8957641351"],
            "error_messages": {
                "pattern": "Invalid Telegram id format. Must contain 10 digits"
            }
        }
    )


# =======================
# User Update Schema
# =======================
class UserUpdate(UserBase):
    """
    Schema for updating user details.
    Allows modification of Telegram link and language preference.
    """
    fullname: Optional[str] = Field(
        None,
        min_length=3, max_length=255,
        pattern=r'^[a-zA-Z\s\'-]+$',
        description='Fullname must contain only letters, spaces, hyphens, and apostrophes',
        json_schema_extra={
            "examples": ["John Doe"],
            "error_messages": {
                "pattern": "Fullname must contain only letters, spaces, hyphens, and apostrophes"
            }
        }
    )

    language_code: Optional[Language] = Field(
        None,
        description="User's preferred language",
        json_schema_extra={
            "examples": ["uz"],
            "error_messages": {
                "invalid_enum": "Invalid language code. Must be one of: en, uz, ru"
            }
        }
    )

    tg_id: Optional[str] = Field(
        None,
        min_length=5, max_length=255,
        description="Telegram id number",
        pattern=r'^\d{8, 12}$',
        json_schema_extra={
            "examples": ["8957641351"],
            "error_messages": {
                "pattern": "Invalid Telegram id format. Must contain 10 digits"
            }
        }
    )


# =======================
# User Phone Number Update Schema
# =======================
class UserPhoneNumberUpdate(BaseModel):
    """
    Schema for updating a user's phone number.
    Ensures the phone number follows Uzbekistan's format.
    """
    new_phone_number: str = Field(
        ...,
        min_length=9, max_length=13,
        pattern=r'^\+998\d{9}$',
        description="Uzbekistan phone number in format: +998901234567",
        json_schema_extra={
            "examples": ["+998901234567"],
            "error_messages": {
                "pattern": "Phone number must be in format: +998901234567"
            }
        }
    )

    password: str = Field(
        ...,
        min_length=6, max_length=255,
        description="Old password",
        json_schema_extra={
            "examples": ["OldPassword123"],
            "error_messages": {
                "minLength": "Password must be at least 6 characters long"
            }
        }
    )


# =======================
# User Password Update Schema
# =======================
class UserPasswordUpdate(BaseModel):
    """
    Schema for updating a user's password.
    Requires both the old and new password.
    """
    old_password: str = Field(
        ...,
        min_length=6, max_length=255,
        description="Old password",
        json_schema_extra={
            "examples": ["OldPassword123"],
            "error_messages": {
                "minLength": "Password must be at least 6 characters long"
            }
        }
    )

    new_password: str = Field(
        ...,
        min_length=6, max_length=255,
        description="New password",
        json_schema_extra={
            "examples": ["NewPassword123"],
            "error_messages": {
                "minLength": "Password must be at least 6 characters long"
            }
        }
    )


# =======================
# User Response Schema
# =======================
class UserResponse(UserBase):
    """
    Schema for returning user details.
    """
    id: int
    fullname: str
    phone_number: str
    tg_id: Optional[str]
    is_admin: bool
    is_active: bool
    is_superuser: bool
    language_code: Language
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)