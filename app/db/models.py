"""
Database models for the application
"""
from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, Float, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    RECRUITER = "recruiter"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Resume(Base):
    """Resume model"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    mime_type = Column(String(50))
    file_path = Column(String(500))
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    analysis_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
