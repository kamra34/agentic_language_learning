"""
User Pydantic schemas for request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.user import AIProvider, CEFRLevel


# Common timezone options
TIMEZONE_OPTIONS = [
    "Europe/Stockholm",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "Europe/Helsinki",
    "Europe/Oslo",
    "Europe/Copenhagen",
    "America/New_York",
    "America/Los_Angeles",
    "America/Chicago",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Australia/Sydney",
    "UTC",
]


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(min_length=8, max_length=100)
    display_name: str | None = Field(None, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    display_name: str | None = Field(None, max_length=100)
    preferred_ai_provider: AIProvider | None = None
    timezone: str | None = Field(None, max_length=50)


class UserResponse(UserBase):
    """Schema for user response (public data)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str | None
    reading_level: CEFRLevel
    writing_level: CEFRLevel
    listening_level: CEFRLevel
    speaking_level: CEFRLevel
    preferred_ai_provider: AIProvider
    timezone: str
    is_active: bool
    created_at: datetime


class UserSkillLevels(BaseModel):
    """Schema for user's CEFR levels."""

    reading: CEFRLevel
    writing: CEFRLevel
    listening: CEFRLevel
    speaking: CEFRLevel


class TokenResponse(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for refreshing access token."""

    refresh_token: str


class SettingsOptions(BaseModel):
    """Schema for available settings options."""

    ai_providers: list[AIProvider] = [AIProvider.CLAUDE, AIProvider.OPENAI]
    timezones: list[str] = TIMEZONE_OPTIONS
