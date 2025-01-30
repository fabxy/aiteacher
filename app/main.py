# Entry point for FastAPI
from fastapi import FastAPI
from app.routes import users, lessons, sql_execution, ai

app = FastAPI(title="SQL Learning App")

# Include routers (API endpoints)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
app.include_router(sql_execution.router, prefix="/sql", tags=["SQL Execution"])
app.include_router(ai.router, prefix="/ai", tags=["AI Lessons"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI-powered SQL Learning App!"}
