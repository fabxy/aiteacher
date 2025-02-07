# Database connection setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define database URLs from environment variables
DB_URLS = {
    "user": os.getenv("DATABASE_URL"),   # User database (sql_learning)
    "super": os.getenv("SUPER_URL"),     # Superuser connection (lesson_sandbox_db)
    "sandbox": os.getenv("SANDBOX_URL"), # sandbox_user connection (lesson_sandbox_db)
    "llm": os.getenv("LLM_URL"),         # llm_user connection (lesson_sandbox_db)
}

# Define a base model for ORM
Base = declarative_base()

# Helper function to create database engines and sessions
def create_db_engine(db_url):
    """Create and return a SQLAlchemy database engine and session maker."""
    engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

# Create engines and session makers for all databases
db_engines = {}
db_sessions = {}

for key, url in DB_URLS.items():
    db_engines[key], db_sessions[key] = create_db_engine(url)

# Dependency Injectors for FastAPI
def get_db(db_type="user"):
    """Generic function to get a database session."""
    db = db_sessions[db_type]()
    try:
        yield db
    finally:
        db.close()
