from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import User, Lesson
from app.schemas import LessonSchema
from app.services.ai_service import generate_ai_lesson, generate_ai_data
import json

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
    
    completed_lessons = db.query(Lesson).filter(Lesson.user_id == lesson.user_id, Lesson.completed == True).all()
    
    user = db.query(User).filter(User.id == lesson.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with lesson ID {lesson.id} not found")
    
    # Generate lesson content
    if not lesson.content:
        try:
            lesson.content = generate_ai_lesson(user, lesson, completed_lessons)
            db.add(lesson)
            db.commit()
            db.refresh(lesson)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error generating lesson content: {str(e)}")
        
    # Create lesson schema in sandbox
    super_session = next(super_db)
    schema_exists = super_session.execute(text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'lesson_{lesson_id}';")).fetchone()

    if not schema_exists:
        try:
            super_session.execute(text(f"CREATE SCHEMA lesson_{lesson_id} AUTHORIZATION waschkowskif;"))
            super_session.execute(text(f"GRANT USAGE, CREATE ON SCHEMA lesson_{lesson_id} TO llm_user;"))
            super_session.execute(text(f"GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO llm_user;"))
            super_session.commit()
        except Exception as e:
            super_session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating schema: {str(e)}")

    # Create exercise table in sandbox
    llm_session = next(llm_db)
    llm_session.execute(text(f"SET search_path TO lesson_{lesson_id};"))
    table_exists = llm_session.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'lesson_{lesson_id}';")).fetchone()
    
    if not table_exists:
        try:
            response = generate_ai_data(lesson)
            queries = json.loads(response).get("queries", [])

            if not queries:
                raise HTTPException(status_code=500, detail="No queries generated for sample data.")
            
            for query in queries:
                llm_session.execute(text(query))
            llm_session.commit()
        except Exception as e:
            llm_session.rollback()
            raise HTTPException(status_code=500, detail=f"Error generating sample data: {str(e)}")

    # Allow sandbox user to access exercise table
    try:
        super_session.execute(text(f"GRANT USAGE ON SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_session.execute(text(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_session.execute(text(f"GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA lesson_{lesson_id} TO sandbox_user;"))
        super_session.commit()
    except Exception as e:
        super_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error granting access to sandbox_user: {str(e)}")
     
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
