from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import User, Lesson
from app.schemas import LessonSchema
from app.services.ai_service import generate_ai_lesson

router = APIRouter()

@router.get("/{lesson_id}", response_model=LessonSchema)
def get_lesson(lesson_id: int, db: Session = Depends(get_db), 
               super_db: Session = Depends(lambda: get_db("super")), 
               llm_db: Session = Depends(lambda: get_db("llm"))):
    """
    Retrieve lesson details by lesson_id.
    If the lesson content is missing, generate it using the AI service.
    """

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    user = db.query(User).filter(User.id == lesson.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with lesson ID {lesson.id} not found")
    
    # Check if lesson was generated already
    if not lesson.content:

        # Generate lesson content
        lesson.content = generate_ai_lesson(user, lesson)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)

        # Create lesson schema in sandbox 
        # TODO: change super user name
        super_db.execute(text(f"CREATE SCHEMA lesson_{lesson_id} AUTHORIZATION waschkowskif;"))
        super_db.execute(text(f"GRANT USAGE, CREATE ON SCHEMA lesson_{lesson_id} TO llm_user;"))
        super_db.execute(text(f"GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO llm_user;"))
        super_db.commit()

        # Create exercise table in sandbox
        llm_db.execute(text(f"SET search_path TO lesson_{lesson_id};"))
        llm_db.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(50),
                salary INTEGER
            );
            """)
        llm_db.execute("""
            INSERT INTO employees (name, department, salary) 
            SELECT * FROM (VALUES
                ('Alice Johnson', 'Engineering', 75000),
                ('Bob Smith', 'Marketing', 60000),
                ('Charlie Brown', 'HR', 50000),
                ('Dana White', 'Finance', 80000)
            ) AS tmp(name, department, salary)
            WHERE NOT EXISTS (SELECT 1 FROM employees);
            """)
        llm_db.commit()

        # Allow sandbox user to access exercise table
        super_db.execute(text(f"GRANT USAGE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_db.commit()
    
    return lesson

@router.post("/{lesson_id}/run_query")
def run_query(lesson_id: int, payload: dict, db: Session = Depends(lambda: get_db("sandbox"))):
    """
    Execute a user-provided SQL query in a dedicated schema for each lesson.
    """

    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="No query provided")
    
    try:
        # Set the schema for execution
        db.execute(text(f"SET search_path TO lesson_{lesson_id};"))

        # Execute the query
        result = db.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in rows]
        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")

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
    
    return None
