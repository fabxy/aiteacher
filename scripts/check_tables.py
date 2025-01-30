import sys
import os
from sqlalchemy import inspect
from dotenv import load_dotenv

# Ensure correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine

# Load environment variables
load_dotenv()

# Print the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔍 Using DATABASE_URL: {DATABASE_URL}")

# Check existing tables
inspector = inspect(engine)
tables = inspector.get_table_names()

if tables:
    print("✅ Tables found in the database:", tables)
else:
    print("❌ No tables exist in the database!")
