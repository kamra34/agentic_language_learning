"""
Chat Pydantic schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.chat import BotType, MessageRole


class MessageBase(BaseModel):
    """Base message schema."""

    content: str = Field(min_length=1, max_length=10000)


class MessageCreate(MessageBase):
    """Schema for creating a message."""

    pass


class MessageResponse(MessageBase):
    """Schema for message response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: MessageRole
    created_at: datetime


class ChatSessionCreate(BaseModel):
    """Schema for creating a chat session."""

    bot_type: BotType


class ChatSessionResponse(BaseModel):
    """Schema for chat session response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    bot_type: BotType
    title: str | None
    message_count: int
    created_at: datetime
    updated_at: datetime


class ChatSessionWithMessages(ChatSessionResponse):
    """Schema for chat session with messages."""

    messages: list[MessageResponse]


class ChatResponse(BaseModel):
    """Schema for chat completion response."""

    message: MessageResponse
    session_id: int


class BotInfo(BaseModel):
    """Schema for bot information."""

    type: BotType
    name: str
    swedish_name: str
    description: str
    icon: str
