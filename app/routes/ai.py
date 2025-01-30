# LLM integration for custom lessons
from fastapi import APIRouter
from app.services.ai_service import generate_lesson

router = APIRouter()

@router.get("/lesson/")
def get_lesson(user_level: str):
    lesson = generate_lesson(user_level)
    return {"lesson": lesson}
