import sys
import os
from sqlalchemy import inspect

# Ensure correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, Base

# 🚨 EXPLICITLY IMPORT ALL MODELS 🚨
import app.models  # This forces model registration

# Print registered tables before creating them
print("🔍 Registered tables in metadata:", Base.metadata.tables.keys())

print("🔄 Dropping existing tables (if any)...")
Base.metadata.drop_all(bind=engine)

print("🔄 Creating new database tables...")
Base.metadata.create_all(bind=engine)

# Verify tables are created
inspector = inspect(engine)
tables = inspector.get_table_names()

if tables:
    print("✅ Tables created successfully:", tables)
else:
    print("❌ No tables created! Check SQLAlchemy models.")
