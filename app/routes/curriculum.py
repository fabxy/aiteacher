from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Curriculum, Lesson
from app.schemas import CurriculumCreateRequest, CurriculumCreateResponse, CurriculumResponse, LessonSchema
from app.services.ai_service import generate_ai_curriculum
import json

router = APIRouter()

@router.post("/generate/", response_model=CurriculumCreateResponse)
async def generate_curriculum(request: CurriculumCreateRequest, db: Session = Depends(get_db)):
    
    # Create a new user
    new_user = User(
        email=None,  # Email is set later during sign-up
        password_hash=None,  # No password yet
        sql_experience=request.sql_experience,
        programming_experience=request.programming_experience,
        learning_commitment=request.learning_commitment
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate curriculum with AI
    lesson_list = generate_ai_curriculum(new_user)

    if not lesson_list or not isinstance(lesson_list, list):
        raise HTTPException(status_code=500, detail="AI failed to generate a valid curriculum")

    # Store each lesson in the database
    lesson_ids = []
    for lesson_title in lesson_list:
        new_lesson = Lesson(
            title=lesson_title,
            user_id=new_user.id,
            content=None,  # Content is generated on-demand
            completed=False
        )
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)
        lesson_ids.append(new_lesson.id)

    # Create a curriculum entry linking to the new lessons
    new_curriculum = Curriculum(
        user_id=new_user.id,
        lesson_ids=json.dumps(lesson_ids)  # Store lesson IDs as a JSON string
    )
    db.add(new_curriculum)
    db.commit()
    db.refresh(new_curriculum)

    # Return the user ID and curriculum ID to the frontend
    return CurriculumCreateResponse(
        user_id=new_user.id
    )

@router.get("/{user_id}", response_model=CurriculumResponse)
async def get_user_curriculum(user_id: int, db: Session = Depends(get_db)):

    # Find the curriculum for the user
    curriculum = db.query(Curriculum).filter(Curriculum.user_id == user_id).first()

    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Retrieve all lesson details
    lesson_ids = json.loads(curriculum.lesson_ids)
    lessons = db.query(Lesson).filter(Lesson.id.in_(lesson_ids)).all()

    # Return lesson titles and curriculum progress
    return CurriculumResponse(
        user_id=user_id,
        curriculum_id=curriculum.id,
        lessons=lessons
    )