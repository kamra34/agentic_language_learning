"""
Vocabulary API routes.
"""

from fastapi import APIRouter, Query

from src.api.dependencies import CurrentUser, DbSession
from src.models.word import WordStatus
from src.schemas.word import (
    ReviewAnswer,
    ReviewResponse,
    UserWordCreate,
    UserWordResponse,
    VocabularyStats,
    WordCreate,
    WordResponse,
)
from src.services.vocabulary import (
    add_word_to_user,
    create_word,
    get_due_reviews,
    get_user_vocabulary,
    get_user_word,
    get_vocabulary_stats,
    get_words,
    remove_user_word,
    submit_review,
)

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])


# ============================================================================
# Dictionary Words (public read, admin write)
# ============================================================================


@router.get("/words", response_model=list[WordResponse])
async def list_words(
    db: DbSession,
    cefr_level: str | None = Query(None, description="Filter by CEFR level (A1-C2)"),
    part_of_speech: str | None = Query(None, description="Filter by part of speech"),
    search: str | None = Query(None, description="Search in Swedish/English"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[WordResponse]:
    """Get dictionary words with optional filters."""
    words = await get_words(
        db,
        cefr_level=cefr_level,
        part_of_speech=part_of_speech,
        search=search,
        limit=limit,
        offset=offset,
    )
    return [WordResponse.model_validate(w) for w in words]


@router.post("/words", response_model=WordResponse)
async def create_dictionary_word(
    word_data: WordCreate,
    db: DbSession,
    current_user: CurrentUser,  # TODO: Add admin check
) -> WordResponse:
    """Create a new dictionary word (admin only)."""
    word = await create_word(db, word_data)
    return WordResponse.model_validate(word)


# ============================================================================
# User Vocabulary
# ============================================================================


@router.get("/my-words", response_model=list[UserWordResponse])
async def list_my_words(
    db: DbSession,
    current_user: CurrentUser,
    status: WordStatus | None = Query(None, description="Filter by learning status"),
    cefr_level: str | None = Query(None, description="Filter by CEFR level"),
    search: str | None = Query(None, description="Search in Swedish/English"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[UserWordResponse]:
    """Get current user's vocabulary."""
    user_words = await get_user_vocabulary(
        db,
        user_id=current_user.id,
        status=status,
        cefr_level=cefr_level,
        search=search,
        limit=limit,
        offset=offset,
    )
    return [UserWordResponse.model_validate(uw) for uw in user_words]


@router.post("/my-words", response_model=UserWordResponse)
async def add_word_to_my_vocabulary(
    word_data: UserWordCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> UserWordResponse:
    """Add a word to current user's vocabulary."""
    user_word = await add_word_to_user(db, current_user.id, word_data)
    return UserWordResponse.model_validate(user_word)


@router.get("/my-words/{user_word_id}", response_model=UserWordResponse)
async def get_my_word(
    user_word_id: int,
    db: DbSession,
    current_user: CurrentUser,
) -> UserWordResponse:
    """Get a specific word from user's vocabulary."""
    user_word = await get_user_word(db, current_user.id, user_word_id)
    if not user_word:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Word not found in your vocabulary")
    return UserWordResponse.model_validate(user_word)


@router.delete("/my-words/{user_word_id}")
async def remove_word_from_my_vocabulary(
    user_word_id: int,
    db: DbSession,
    current_user: CurrentUser,
) -> dict:
    """Remove a word from current user's vocabulary."""
    success = await remove_user_word(db, current_user.id, user_word_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Word not found in your vocabulary")
    return {"message": "Word removed from vocabulary"}


# ============================================================================
# Review & SRS
# ============================================================================


@router.get("/review", response_model=list[UserWordResponse])
async def get_words_for_review(
    db: DbSession,
    current_user: CurrentUser,
    limit: int = Query(20, ge=1, le=50, description="Number of cards to review"),
) -> list[UserWordResponse]:
    """Get words due for review."""
    due_words = await get_due_reviews(db, current_user.id, limit=limit)
    return [UserWordResponse.model_validate(uw) for uw in due_words]


@router.post("/review/{user_word_id}", response_model=ReviewResponse)
async def submit_word_review(
    user_word_id: int,
    answer: ReviewAnswer,
    db: DbSession,
    current_user: CurrentUser,
) -> ReviewResponse:
    """Submit a review answer for a word."""
    return await submit_review(db, current_user.id, user_word_id, answer)


# ============================================================================
# Statistics
# ============================================================================


@router.get("/stats", response_model=VocabularyStats)
async def get_my_vocabulary_stats(
    db: DbSession,
    current_user: CurrentUser,
) -> VocabularyStats:
    """Get vocabulary statistics for current user."""
    return await get_vocabulary_stats(db, current_user.id)
