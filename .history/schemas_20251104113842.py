"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional


# Authentication Schemas
class UserSignup(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores and hyphens allowed)')
        return v.lower()


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user information"""
    id: int
    username: str
    full_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Chat Schemas
class ChatMessage(BaseModel):
    """Schema for sending a chat message"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")


class MessageResponse(BaseModel):
    """Schema for a single message in history"""
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """Schema for AI response"""
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistoryResponse(BaseModel):
    """Schema for chat history"""
    messages: List[MessageResponse]
    total_messages: int


# Generic Response Schemas
class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """Generic error response"""
    error: str
    detail: Optional[str] = None
