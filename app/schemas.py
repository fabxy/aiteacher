# Pydantic models for request/response validation
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User Registration & Authentication Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    sql_experience: str
    programming_experience: str
    learning_commitment: str
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Ensures SQLAlchemy models work with Pydantic

# Curriculum response schema
class CurriculumResponse(BaseModel):
    user_id: int
    curriculum: List[str]

# Update email schema
class UpdateEmailRequest(BaseModel):
    user_id: int
    email: EmailStr
    password: str

# Login schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

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
