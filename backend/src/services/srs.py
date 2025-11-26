"""
Spaced Repetition System (SRS) using SM-2 algorithm.

The SM-2 algorithm calculates optimal review intervals based on:
- Ease Factor (EF): How easy the card is (2.5 default, min 1.3)
- Quality (q): User's answer quality (0-5 scale)
- Repetition Number (n): How many times successfully reviewed
- Interval (I): Days until next review

Quality ratings:
- 0: Complete blackout, no memory
- 1: Wrong answer, but recognized when shown
- 2: Wrong answer, but easy to remember
- 3: Correct with serious difficulty
- 4: Correct with some hesitation
- 5: Perfect, immediate recall
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class SRSResult:
    """Result of an SRS calculation."""

    ease_factor: float
    interval_days: int
    repetition_number: int
    next_review: datetime
    status: str


def calculate_sm2(
    quality: int,
    ease_factor: float = 2.5,
    interval_days: int = 1,
    repetition_number: int = 0,
) -> SRSResult:
    """
    Calculate next review interval using SM-2 algorithm.

    Args:
        quality: Answer quality (0-5)
        ease_factor: Current ease factor (default 2.5)
        interval_days: Current interval in days
        repetition_number: Current repetition count

    Returns:
        SRSResult with updated SRS values
    """
    # Clamp quality to valid range
    quality = max(0, min(5, quality))

    # Calculate new ease factor
    # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)  # Minimum ease factor is 1.3

    # Determine if answer was successful (quality >= 3)
    if quality >= 3:
        # Successful recall
        if repetition_number == 0:
            new_interval = 1
        elif repetition_number == 1:
            new_interval = 6
        else:
            new_interval = round(interval_days * new_ef)

        new_repetition = repetition_number + 1
        status = _determine_status(new_repetition, quality)
    else:
        # Failed recall - reset to beginning
        new_interval = 1
        new_repetition = 0
        status = "review_needed"

    # Calculate next review date
    next_review = datetime.now(timezone.utc) + timedelta(days=new_interval)

    return SRSResult(
        ease_factor=round(new_ef, 2),
        interval_days=new_interval,
        repetition_number=new_repetition,
        next_review=next_review,
        status=status,
    )


def _determine_status(repetition_number: int, quality: int) -> str:
    """Determine word status based on repetition count and quality."""
    if repetition_number == 0:
        return "new"
    elif repetition_number <= 2:
        return "learning"
    elif repetition_number <= 5:
        return "familiar"
    else:
        # Check if consistently getting high quality answers
        if quality >= 4:
            return "mastered"
        return "familiar"


def get_due_cards_query_filter(user_id: int):
    """
    Get SQLAlchemy filter for cards due for review.

    Usage:
        query = select(UserWord).where(
            UserWord.user_id == user_id,
            get_due_cards_query_filter(user_id)
        )
    """
    from sqlalchemy import or_

    from src.models.word import UserWord

    now = datetime.now(timezone.utc)

    return or_(
        UserWord.next_review.is_(None),  # Never reviewed
        UserWord.next_review <= now,  # Due for review
    )


def calculate_retention_score(
    times_correct: int, times_incorrect: int, ease_factor: float
) -> float:
    """
    Calculate a retention score (0-100) for a word.

    Combines accuracy with ease factor for a holistic score.
    """
    total = times_correct + times_incorrect
    if total == 0:
        return 0.0

    accuracy = times_correct / total
    # Normalize ease factor (1.3-2.5+ range to 0-1)
    ef_normalized = min((ease_factor - 1.3) / 1.7, 1.0)

    # Weighted combination: 70% accuracy, 30% ease factor
    score = (accuracy * 0.7 + ef_normalized * 0.3) * 100
    return round(score, 1)
