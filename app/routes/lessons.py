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
        super_session = next(super_db)
        
        # NOTE: Only works when React Strict mode is disabled
        super_session.execute(text(f"CREATE SCHEMA lesson_{lesson_id} AUTHORIZATION waschkowskif;"))
        super_session.execute(text(f"GRANT USAGE, CREATE ON SCHEMA lesson_{lesson_id} TO llm_user;"))
        super_session.execute(text(f"GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO llm_user;"))
        super_session.commit()

        # Create exercise table in sandbox
        llm_session = next(llm_db)
        llm_session.execute(text(f"SET search_path TO lesson_{lesson_id};"))
        llm_session.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(50),
                salary INTEGER
            );
            """))
        llm_session.execute(text("""
            INSERT INTO employees (name, department, salary) 
            SELECT * FROM (VALUES
                ('Alice Johnson', 'Engineering', 75000),
                ('Bob Smith', 'Marketing', 60000),
                ('Charlie Brown', 'HR', 50000),
                ('Dana White', 'Finance', 80000)
            ) AS tmp(name, department, salary)
            WHERE NOT EXISTS (SELECT 1 FROM employees);
            """))
        llm_session.commit()

        # Allow sandbox user to access exercise table
        super_session.execute(text(f"GRANT USAGE ON SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_session.execute(text(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_session.execute(text(f"GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA lesson_{lesson_id} TO sandbox_user;"))

        super_session.commit()

    print(lesson.content)
    
    return lesson

@router.post("/{lesson_id}/run_query")
def run_query(lesson_id: int, payload: dict, sandbox_db: Session = Depends(lambda: get_db("sandbox"))):
    """
    Execute a user-provided SQL query in a dedicated schema for each lesson.
    """

    query = payload.get("query")

    if not query:
        raise HTTPException(status_code=400, detail="No query provided")
    
    try:
        # Set the schema for execution
        sandbox_session = next(sandbox_db)
        sandbox_session.execute(text(f"SET search_path TO lesson_{lesson_id};"))

        # Detect if it's an INSERT, UPDATE, or DELETE query
        query_type = query.strip().split()[0].upper()

        # Execute the query
        result = sandbox_session.execute(text(query))

        if query_type == "SELECT":
            rows = result.fetchall()
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
        else:
            sandbox_session.commit()
            data = "Query executed successfully"
        
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
