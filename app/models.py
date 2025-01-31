from sqlalchemy import Column, Integer, String, ForeignKey, Text
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
    
class Curriculum(Base):
    __tablename__ = "curriculums"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    lessons = Column(Text)  # JSON-encoded list of lesson titles

    user = relationship("User", back_populates="curriculum")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(Integer, default=0)

    user = relationship("User")
