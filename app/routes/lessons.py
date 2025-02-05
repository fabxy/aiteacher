from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import User, Lesson
from app.services.ai_service import generate_ai_lesson

router = APIRouter()

@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """
    Retrieve lesson details by lesson_id.
    If the lesson content is missing, generate it using the AI service.
    """

    print("lesson_id", lesson_id)

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    user = db.query(User).filter(User.id == lesson.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with lesson ID {lesson.id} not found")
    
    # Check if content exists; if not, generate it.
    if not lesson.content:
        lesson.content = generate_ai_lesson(user, lesson)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "completed": lesson.completed
    }

# @router.post("/lessons/{lesson_id}/run_query")
# def run_query(lesson_id: int, payload: dict, db: Session = Depends(get_db)):
#     """
#     Execute a user-provided SQL query and return the results.
#     Only SELECT queries are allowed for safety.
#     """
#     # Verify the lesson exists.
#     lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
#     if not lesson:
#         raise HTTPException(status_code=404, detail="Lesson not found")
    
#     query = payload.get("query")
#     if not query:
#         raise HTTPException(status_code=400, detail="No query provided")
    
#     try:
#         # For security, allow only SELECT queries.
#         if not query.strip().lower().startswith("select"):
#             raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
        
#         # Execute the query using SQLAlchemy's text module.
#         result = db.execute(text(query))
#         rows = result.fetchall()
#         columns = result.keys()
#         data = [dict(zip(columns, row)) for row in rows]
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")

@router.put("/{lesson_id}/complete")
def mark_lesson_complete(lesson_id: int, db: Session = Depends(get_db)):
    """
    Mark the specified lesson as completed.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson.completed = True
    db.commit()
    db.refresh(lesson)
    
    return {
        "message": "Lesson marked as complete",
        "lesson": {
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "completed": lesson.completed
        }
    }
