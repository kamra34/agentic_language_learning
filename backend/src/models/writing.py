"""
Writing submission and analysis models.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.db.session import Base


class WritingSubmission(Base):
    """A user's writing submission with analysis."""

    __tablename__ = "writing_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    chat_session_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_sessions.id"), nullable=True
    )

    # Content
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    corrected_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Analysis results (stored as JSON)
    spelling_errors: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    grammar_errors: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    vocabulary_feedback: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Scores
    spelling_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    grammar_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    vocabulary_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    complexity_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # CEFR estimate for this writing
    cefr_estimate: Mapped[str | None] = mapped_column(String(2), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<WritingSubmission {self.id} user={self.user_id}>"


class UserSpellingPattern(Base):
    """Track user's common spelling mistakes for targeted practice."""

    __tablename__ = "user_spelling_patterns"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    correct_word: Mapped[str] = mapped_column(String(100), nullable=False)
    common_misspelling: Mapped[str] = mapped_column(String(100), nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, default=1)

    # Error category (vowels, consonants, swedish_specific like å/ä/ö)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Timestamps
    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<UserSpellingPattern {self.common_misspelling} -> {self.correct_word}>"
