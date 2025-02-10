# Pydantic models for request/response validation
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# User schemas
class SignupRequest(BaseModel):
    user_id: int
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user_id: int

# Lesson schemas
class LessonSchema(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str] = None
    completed: bool

    model_config = ConfigDict(from_attributes=True)

# Curriculum schemas
class CurriculumCreateRequest(BaseModel):
    sql_experience: str
    programming_experience: str
    learning_goals: str
    learning_commitment: str

class CurriculumCreateResponse(BaseModel):
    user_id: int

class CurriculumResponse(BaseModel):
    user_id: int                        # unnecessary?
    curriculum_id: int
    lessons: List[LessonSchema]