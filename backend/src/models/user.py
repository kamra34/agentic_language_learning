"""
User database model.
"""

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.session import Base


class CEFRLevel(str, Enum):
    """CEFR language proficiency levels."""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # CEFR levels per skill
    reading_level: Mapped[str] = mapped_column(String(2), default=CEFRLevel.A1.value)
    writing_level: Mapped[str] = mapped_column(String(2), default=CEFRLevel.A1.value)
    listening_level: Mapped[str] = mapped_column(String(2), default=CEFRLevel.A1.value)
    speaking_level: Mapped[str] = mapped_column(String(2), default=CEFRLevel.A1.value)

    # Account status
    is_active: Mapped[bool] = mapped_column(default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
