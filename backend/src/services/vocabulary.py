"""
Vocabulary service for word management and SRS reviews.
"""

from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import NotFoundException
from src.models.word import UserWord, Word, WordStatus
from src.schemas.word import (
    ReviewAnswer,
    ReviewResponse,
    UserWordCreate,
    VocabularyStats,
    WordCreate,
)
from src.services.srs import calculate_sm2


# ============================================================================
# Word CRUD (admin operations)
# ============================================================================


async def create_word(db: AsyncSession, word_data: WordCreate) -> Word:
    """Create a new word in the dictionary."""
    word = Word(**word_data.model_dump())
    db.add(word)
    await db.flush()
    await db.refresh(word)
    return word


async def get_word_by_id(db: AsyncSession, word_id: int) -> Word | None:
    """Get a word by ID."""
    result = await db.execute(select(Word).where(Word.id == word_id))
    return result.scalar_one_or_none()


async def get_words(
    db: AsyncSession,
    cefr_level: str | None = None,
    part_of_speech: str | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Word]:
    """Get words with optional filters."""
    query = select(Word)

    if cefr_level:
        query = query.where(Word.cefr_level == cefr_level)
    if part_of_speech:
        query = query.where(Word.part_of_speech == part_of_speech)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Word.swedish.ilike(search_pattern),
                Word.english.ilike(search_pattern),
            )
        )

    query = query.order_by(Word.frequency_rank.asc().nulls_last()).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def bulk_create_words(db: AsyncSession, words_data: list[WordCreate]) -> int:
    """Bulk create words. Returns count of created words."""
    words = [Word(**word_data.model_dump()) for word_data in words_data]
    db.add_all(words)
    await db.flush()
    return len(words)


# ============================================================================
# User Vocabulary
# ============================================================================


async def add_word_to_user(
    db: AsyncSession, user_id: int, word_data: UserWordCreate
) -> UserWord:
    """Add a word to user's vocabulary."""
    # Check if word exists
    word = await get_word_by_id(db, word_data.word_id)
    if not word:
        raise NotFoundException(f"Word with id {word_data.word_id} not found")

    # Check if already added
    existing = await db.execute(
        select(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.word_id == word_data.word_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("Word already in user's vocabulary")

    user_word = UserWord(
        user_id=user_id,
        word_id=word_data.word_id,
        status=WordStatus.NEW.value,
    )
    db.add(user_word)
    await db.flush()
    await db.refresh(user_word, ["word"])
    return user_word


async def get_user_vocabulary(
    db: AsyncSession,
    user_id: int,
    status: WordStatus | None = None,
    cefr_level: str | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[UserWord]:
    """Get user's vocabulary with optional filters."""
    query = (
        select(UserWord)
        .options(selectinload(UserWord.word))
        .where(UserWord.user_id == user_id)
    )

    if status:
        query = query.where(UserWord.status == status.value)

    if cefr_level or search:
        query = query.join(Word)
        if cefr_level:
            query = query.where(Word.cefr_level == cefr_level)
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Word.swedish.ilike(search_pattern),
                    Word.english.ilike(search_pattern),
                )
            )

    query = query.order_by(UserWord.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_user_word(
    db: AsyncSession, user_id: int, user_word_id: int
) -> UserWord | None:
    """Get a specific user word by ID."""
    result = await db.execute(
        select(UserWord)
        .options(selectinload(UserWord.word))
        .where(
            UserWord.id == user_word_id,
            UserWord.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def remove_user_word(db: AsyncSession, user_id: int, user_word_id: int) -> bool:
    """Remove a word from user's vocabulary."""
    user_word = await get_user_word(db, user_id, user_word_id)
    if not user_word:
        return False
    await db.delete(user_word)
    await db.flush()
    return True


# ============================================================================
# SRS Review
# ============================================================================


async def get_due_reviews(
    db: AsyncSession,
    user_id: int,
    limit: int = 20,
) -> list[UserWord]:
    """Get words due for review."""
    now = datetime.now(timezone.utc)

    query = (
        select(UserWord)
        .options(selectinload(UserWord.word))
        .where(
            UserWord.user_id == user_id,
            or_(
                UserWord.next_review.is_(None),  # Never reviewed
                UserWord.next_review <= now,  # Due for review
            ),
        )
        .order_by(
            # Prioritize: overdue > new > by next_review date
            UserWord.next_review.asc().nulls_last()
        )
        .limit(limit)
    )

    result = await db.execute(query)
    return list(result.scalars().all())


async def submit_review(
    db: AsyncSession,
    user_id: int,
    user_word_id: int,
    answer: ReviewAnswer,
) -> ReviewResponse:
    """Submit a review answer and update SRS values."""
    user_word = await get_user_word(db, user_id, user_word_id)
    if not user_word:
        raise NotFoundException(f"UserWord with id {user_word_id} not found")

    # Calculate new SRS values
    srs_result = calculate_sm2(
        quality=answer.quality,
        ease_factor=user_word.ease_factor,
        interval_days=user_word.interval_days,
        repetition_number=user_word.repetition_number,
    )

    # Update user word
    user_word.ease_factor = srs_result.ease_factor
    user_word.interval_days = srs_result.interval_days
    user_word.repetition_number = srs_result.repetition_number
    user_word.next_review = srs_result.next_review
    user_word.last_reviewed = datetime.now(timezone.utc)
    user_word.status = srs_result.status
    user_word.times_seen += 1

    if answer.quality >= 3:
        user_word.times_correct += 1
    else:
        user_word.times_incorrect += 1

    await db.flush()
    await db.refresh(user_word)

    return ReviewResponse(
        user_word_id=user_word.id,
        new_status=WordStatus(user_word.status),
        next_review=srs_result.next_review,
        interval_days=srs_result.interval_days,
    )


# ============================================================================
# Statistics
# ============================================================================


async def get_vocabulary_stats(db: AsyncSession, user_id: int) -> VocabularyStats:
    """Get vocabulary statistics for a user."""
    now = datetime.now(timezone.utc)

    # Count by status
    status_counts = await db.execute(
        select(UserWord.status, func.count(UserWord.id))
        .where(UserWord.user_id == user_id)
        .group_by(UserWord.status)
    )
    counts = {row[0]: row[1] for row in status_counts.all()}

    # Count due for review
    due_count_result = await db.execute(
        select(func.count(UserWord.id)).where(
            UserWord.user_id == user_id,
            or_(
                UserWord.next_review.is_(None),
                UserWord.next_review <= now,
            ),
        )
    )
    due_count = due_count_result.scalar() or 0

    return VocabularyStats(
        total_words=sum(counts.values()),
        new=counts.get(WordStatus.NEW.value, 0),
        learning=counts.get(WordStatus.LEARNING.value, 0),
        familiar=counts.get(WordStatus.FAMILIAR.value, 0),
        mastered=counts.get(WordStatus.MASTERED.value, 0),
        review_needed=counts.get(WordStatus.REVIEW_NEEDED.value, 0),
        due_for_review=due_count,
    )
