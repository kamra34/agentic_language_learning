"""
API dependencies for authentication and database access.
"""

from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import CredentialsException
from src.core.security import decode_token
from src.db.session import get_db
from src.models.user import User
from src.services.auth import get_user_by_id


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token."""
    if not authorization:
        raise CredentialsException("Authorization header missing")

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise CredentialsException("Invalid authorization header format")

    token = parts[1]
    payload = decode_token(token)
    if not payload:
        raise CredentialsException("Invalid or expired token")

    if payload.get("type") != "access":
        raise CredentialsException("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise CredentialsException("Invalid token payload")

    user = await get_user_by_id(db, int(user_id))
    if not user:
        raise CredentialsException("User not found")

    if not user.is_active:
        raise CredentialsException("User account is disabled")

    return user


# Type alias for dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
