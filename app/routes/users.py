# User authentication & profiles
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import SignupRequest, LoginRequest, LoginResponse
from passlib.context import CryptContext
import bcrypt
if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup/")
def update_email(request: SignupRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)
    
    # Update user
    user.email = request.email
    user.password_hash = hashed_password
    db.commit()
    
    return None


@router.post("/login/", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return LoginResponse(user_id=user.id)