from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://your_user:your_password@localhost:5432/sql_learning")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

