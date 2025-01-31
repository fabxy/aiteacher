# Entry point for FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, lessons, sql_execution, ai

app = FastAPI(title="SQL Learning App")

# Allow frontend to communicate with backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains (use specific domains in production, e.g. ["http://localhost:3000", "https://myfrontend.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# Include routers (API endpoints)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
app.include_router(sql_execution.router, prefix="/sql", tags=["SQL Execution"])
app.include_router(ai.router, prefix="/ai", tags=["AI Lessons"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI-powered SQL Learning App!"}
