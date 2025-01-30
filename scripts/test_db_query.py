import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Ensure correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://my_user:my_password@localhost:5432/sql_learning")

# Connect to database
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database();"))
        db_name = result.scalar()
        print(f"✅ Successfully connected to database: {db_name}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

