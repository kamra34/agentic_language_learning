"""
Skill level tracking models.
"""

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.db.session import Base


class SkillType(str, Enum):
    """The four language skills."""

    READING = "reading"
    WRITING = "writing"
    LISTENING = "listening"
    SPEAKING = "speaking"


class SkillAssessment(Base):
    """Individual skill assessment record."""

    __tablename__ = "skill_assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    skill: Mapped[str] = mapped_column(String(20), nullable=False)
    cefr_level: Mapped[str] = mapped_column(String(2), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)

    # Assessment details (what triggered this assessment)
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Timestamp
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<SkillAssessment {self.skill}={self.cefr_level}>"
