from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    """Single chat message model"""
    role: str  # "user" or "assistant"
    content: str  # The actual message text
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    """Chat session model for database"""
    session_id: str  # Unique ID for this conversation
    user_id: str  # Who is chatting
    messages: List[Message] = []  # All messages in this session
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    """What the API expects when user sends a message"""
    user_id: str
    message: str
    session_id: Optional[str] = None  # Optional - new session if not provided

class ChatResponse(BaseModel):
    """What the API returns to the user"""
    session_id: str
    user_id: str
    message: str  # Original user message
    response: str  # Bot's answer
    timestamp: datetime