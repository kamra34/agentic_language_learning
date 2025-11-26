"""
Vocabulary word models.
"""

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base


class Gender(str, Enum):
    """Swedish noun genders."""

    EN = "en"
    ETT = "ett"


class PartOfSpeech(str, Enum):
    """Parts of speech."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    NUMERAL = "numeral"


class WordStatus(str, Enum):
    """User's learning status for a word."""

    NEW = "new"
    LEARNING = "learning"
    FAMILIAR = "familiar"
    MASTERED = "mastered"
    REVIEW_NEEDED = "review_needed"


class Word(Base):
    """Swedish vocabulary word."""

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    swedish: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    english: Mapped[str] = mapped_column(String(255), nullable=False)
    pronunciation: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Linguistic properties
    part_of_speech: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(3), nullable=True)  # en/ett

    # CEFR and frequency
    cefr_level: Mapped[str] = mapped_column(String(2), default="A1")
    frequency_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Examples and context
    example_sv: Mapped[str | None] = mapped_column(Text, nullable=True)
    example_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user_words: Mapped[list["UserWord"]] = relationship("UserWord", back_populates="word")

    def __repr__(self) -> str:
        return f"<Word {self.swedish} ({self.english})>"


class UserWord(Base):
    """User's progress on a specific word (SRS tracking)."""

    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"), index=True, nullable=False)

    # Learning status
    status: Mapped[str] = mapped_column(String(20), default=WordStatus.NEW.value)

    # SRS statistics
    times_seen: Mapped[int] = mapped_column(Integer, default=0)
    times_correct: Mapped[int] = mapped_column(Integer, default=0)
    times_incorrect: Mapped[int] = mapped_column(Integer, default=0)

    # SRS scheduling (SM-2 algorithm values)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=1)
    repetition_number: Mapped[int] = mapped_column(Integer, default=0)

    # Review dates
    last_reviewed: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_review: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # User's personal notes
    user_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

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

    # Relationships
    word: Mapped["Word"] = relationship("Word", back_populates="user_words")

    def __repr__(self) -> str:
        return f"<UserWord user={self.user_id} word={self.word_id} status={self.status}>"
