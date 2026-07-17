"""
Health check routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    return {"status": "ok", "service": "Resume Analyzer API"}
