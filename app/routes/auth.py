"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(email: str, username: str, password: str, db: Session = Depends(get_db)):
    """Register a new user"""
    # TODO: Implement user registration
    return {"message": "Registration endpoint"}


@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login user"""
    # TODO: Implement user login
    return {"message": "Login endpoint"}
