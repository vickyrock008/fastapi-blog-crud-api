from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Auth
class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

# Posts
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Comments / Likes
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)

class CommentOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
