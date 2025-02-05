import sys
import os
from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker

# Ensure correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, Base

# 🚨 EXPLICITLY IMPORT ALL MODELS 🚨
import app.models  # This forces model registration

# Create a session to execute raw SQL
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Step 1: Drop all tables with CASCADE
print("🔄 Dropping all tables with CASCADE...")

try:
    session.execute(text("DROP SCHEMA public CASCADE;"))
    session.execute(text("CREATE SCHEMA public;"))
    session.commit()
    print("✅ All tables dropped successfully!")
except Exception as e:
    session.rollback()
    print(f"❌ Error dropping tables: {e}")

# Step 2: Recreate Tables
print("🔄 Creating new database tables...")
Base.metadata.create_all(bind=engine)

# Verify tables are created
inspector = inspect(engine)
tables = inspector.get_table_names()

if tables:
    print("✅ Tables created successfully:", tables)
else:
    print("❌ No tables created! Check SQLAlchemy models.")

# Close session
session.close()
