"""
Authentication routes.
"""

from fastapi import APIRouter

from src.api.dependencies import CurrentUser, DbSession
from src.schemas.user import (
    SettingsOptions,
    TokenRefresh,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from src.services.auth import (
    authenticate_user,
    create_tokens,
    create_user,
    refresh_access_token,
    update_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: DbSession) -> TokenResponse:
    """Register a new user account."""
    user = await create_user(db, user_data)
    return create_tokens(user)


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: DbSession) -> TokenResponse:
    """Login with email and password."""
    user = await authenticate_user(db, credentials.email, credentials.password)
    return create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(token_data: TokenRefresh, db: DbSession) -> TokenResponse:
    """Refresh access token using refresh token."""
    return await refresh_access_token(db, token_data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """Get current user's profile information."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
) -> UserResponse:
    """Update current user's profile."""
    updated_user = await update_user(db, current_user, user_data)
    return UserResponse.model_validate(updated_user)


@router.get("/settings/options", response_model=SettingsOptions)
async def get_settings_options() -> SettingsOptions:
    """Get available settings options (AI providers, timezones)."""
    return SettingsOptions()
