# User authentication & profiles
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Curriculum
from app.schemas import UserCreate, UpdateEmailRequest, LoginRequest
from app.services.ai_service import generate_curriculum
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/generate_curriculum/")
def generate_curriculum_route(user_data: UserCreate, db: Session = Depends(get_db)):
    # Create a new user without an email
    new_user = User(
        sql_experience=user_data.sql_experience,
        programming_experience=user_data.programming_experience,
        learning_commitment=user_data.learning_commitment,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate curriculum
    curriculum_data = generate_curriculum(new_user.sql_experience, new_user.programming_experience, new_user.learning_commitment)
    new_curriculum = Curriculum(user_id=new_user.id, title="Personalized SQL Curriculum", lessons=curriculum_data)
    db.add(new_curriculum)
    db.commit()

    return {"user_id": new_user.id, "curriculum": curriculum_data}

@router.get("/curriculum/{user_id}")
def get_user_curriculum(user_id: int, db: Session = Depends(get_db)):
    curriculum = db.query(Curriculum).filter(Curriculum.user_id == user_id).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    return {"title": curriculum.title, "lessons": curriculum.lessons}

@router.post("/update_email/")
def update_email(request: UpdateEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)
    
    # Update user
    user.email = request.email
    user.password_hash = hashed_password
    db.commit()
    
    return {"message": "Email & password updated successfully"}



@router.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"user_id": user.id, "message": "Login successful"}