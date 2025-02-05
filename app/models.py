from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    sql_experience = Column(Text)
    programming_experience = Column(Text)
    learning_commitment = Column(Text)

    curriculum = relationship("Curriculum", back_populates="user")
    lessons = relationship("Lesson", back_populates="user")
    
class Curriculum(Base):
    __tablename__ = "curriculums"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_ids = Column(Text)  # Store lesson IDs as a JSON list

    user = relationship("User", back_populates="curriculum")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="lessons")
