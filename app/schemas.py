# Pydantic models for request/response validation
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User Registration & Authentication Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Password should be hashed before storing

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Ensures SQLAlchemy models work with Pydantic

# Lesson Schemas
class LessonBase(BaseModel):
    title: str
    content: str

class LessonCreate(LessonBase):
    pass  # No additional fields needed for creation

class LessonResponse(LessonBase):
    id: int

    class Config:
        from_attributes = True

# Progress Tracking Schemas
class ProgressBase(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool

class ProgressCreate(ProgressBase):
    pass  # No additional fields needed

class ProgressResponse(ProgressBase):
    id: int

    class Config:
        from_attributes = True

# AI Lesson Request Schema
class LessonRequest(BaseModel):
    user_level: str  # Beginner, Intermediate, Advanced

# SQL Execution Request & Response
class SQLQuery(BaseModel):
    query: str

class SQLResponse(BaseModel):
    result: Optional[List[List[str]]] = None
    error: Optional[str] = None
