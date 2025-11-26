"""
Vocabulary word Pydantic schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.word import Gender, PartOfSpeech, WordStatus


class WordBase(BaseModel):
    """Base word schema."""

    swedish: str = Field(max_length=100)
    english: str = Field(max_length=255)
    pronunciation: str | None = Field(None, max_length=100)
    part_of_speech: PartOfSpeech | None = None
    gender: Gender | None = None
    cefr_level: str = Field(default="A1", max_length=2)
    example_sv: str | None = None
    example_en: str | None = None
    notes: str | None = None


class WordCreate(WordBase):
    """Schema for creating a word."""

    frequency_rank: int | None = None


class WordResponse(WordBase):
    """Schema for word response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    frequency_rank: int | None
    created_at: datetime


class UserWordBase(BaseModel):
    """Base user word schema."""

    status: WordStatus = WordStatus.NEW
    user_notes: str | None = None


class UserWordCreate(BaseModel):
    """Schema for adding a word to user's vocabulary."""

    word_id: int


class UserWordUpdate(BaseModel):
    """Schema for updating user's word progress."""

    status: WordStatus | None = None
    user_notes: str | None = None


class UserWordResponse(BaseModel):
    """Schema for user word response with SRS data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    word_id: int
    status: WordStatus
    times_seen: int
    times_correct: int
    times_incorrect: int
    ease_factor: float
    interval_days: int
    last_reviewed: datetime | None
    next_review: datetime | None
    user_notes: str | None
    created_at: datetime
    word: WordResponse


class ReviewAnswer(BaseModel):
    """Schema for submitting a review answer."""

    quality: int = Field(ge=0, le=5, description="Answer quality: 0=blackout, 5=perfect")


class ReviewResponse(BaseModel):
    """Schema for review result."""

    user_word_id: int
    new_status: WordStatus
    next_review: datetime
    interval_days: int


class VocabularyStats(BaseModel):
    """Schema for vocabulary statistics."""

    total_words: int
    new: int
    learning: int
    familiar: int
    mastered: int
    review_needed: int
    due_for_review: int
