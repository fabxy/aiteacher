# Lesson generation & retrieval
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lesson
from app.schemas import LessonCreate, LessonResponse
from typing import List

router = APIRouter()

# Create a new lesson
@router.post("/", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = Lesson(title=lesson.title, content=lesson.content)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# Get all lessons
@router.get("/", response_model=List[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).all()
    return lessons

# Get a single lesson by ID
@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
