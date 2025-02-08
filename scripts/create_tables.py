import sys
import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Ensure correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import db_engines, Base  # Import all database engines

# 🚨 EXPLICITLY IMPORT ALL MODELS 🚨
import app.models  # This forces model registration

# Get the correct database engines (superuser connections)
super_user_engine = db_engines["super"]  # Superuser for lesson_sandbox_db
user_db_engine = db_engines["user"]  # Superuser for sql_learning

# Create sessions for raw SQL execution
SuperSession = sessionmaker(bind=super_user_engine)
UserSession = sessionmaker(bind=user_db_engine)

super_session = SuperSession()
user_session = UserSession()

### **Step 1: Drop and Recreate Both Databases** ###
def reset_database(session, db_name, sandbox=False):
    """Drops all schemas and tables in the specified database and recreates the public schema."""
    print(f"🔄 Dropping all schemas and tables in {db_name}...")

    try:
        # Remove all user-created lesson schemas in lesson_sandbox_db
        if sandbox:
            schemas_to_drop = session.execute(text(
                "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'lesson_%';"
            )).fetchall()

            for schema in schemas_to_drop:
                schema_name = schema[0]
                print(f"🚮 Dropping schema: {schema_name}")
                session.execute(text(f"DROP SCHEMA {schema_name} CASCADE;"))

        # Drop and recreate the public schema
        session.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
        session.execute(text("CREATE SCHEMA public;"))

        session.commit()
        print(f"✅ {db_name} reset successfully!")

    except Exception as e:
        session.rollback()
        print(f"❌ Error resetting {db_name}: {e}")

# Reset both databases
reset_database(user_session, "sql_learning")
reset_database(super_session, "lesson_sandbox_db", sandbox=True)  # Clean all lesson schemas

### **Step 2: Recreate Tables for sql_learning (User Database)** ###
print("🔄 Creating new tables in sql_learning...")
Base.metadata.create_all(bind=user_db_engine)

# Verify tables in sql_learning
inspector = inspect(user_db_engine)
tables = inspector.get_table_names()

if tables:
    print("✅ Tables created successfully in sql_learning:", tables)
else:
    print("❌ No tables created in sql_learning! Check SQLAlchemy models.")

# Close sessions
super_session.close()
user_session.close()

print("✅ Full database reset complete!")
