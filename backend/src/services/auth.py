"""
Authentication service.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, CredentialsException
from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from src.models.user import User
from src.schemas.user import TokenResponse, UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Get user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    # Check if email already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ConflictException("Email already registered")

    # Create user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        display_name=user_data.display_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Authenticate user with email and password."""
    user = await get_user_by_email(db, email)
    if not user:
        raise CredentialsException("Invalid email or password")

    if not verify_password(password, user.hashed_password):
        raise CredentialsException("Invalid email or password")

    if not user.is_active:
        raise CredentialsException("Account is disabled")

    return user


def create_tokens(user: User) -> TokenResponse:
    """Create access and refresh tokens for user."""
    token_data = {"sub": str(user.id), "email": user.email}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> TokenResponse:
    """Refresh access token using refresh token."""
    payload = decode_token(refresh_token)
    if not payload:
        raise CredentialsException("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise CredentialsException("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise CredentialsException("Invalid token payload")

    user = await get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        raise CredentialsException("User not found or inactive")

    return create_tokens(user)
