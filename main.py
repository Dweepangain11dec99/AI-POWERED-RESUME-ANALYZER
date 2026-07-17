"""
Main application entry point
FastAPI web application with PostgreSQL database
"""
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from typing import AsyncGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database initialization
from app.db.database import init_db, get_db, engine, Base
from app.routes import get_all_routers
from app.middleware.error_handling import error_handler
from app.api_docs import custom_openapi


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup logic
    logger.info("Starting up application...")
    try:
        # Initialize database tables
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    
    # Run environment checks (spaCy models, required packages)
    try:
        from app.services.environment_checks import run_startup_checks
        run_startup_checks()
        logger.info("Environment checks passed")
    except Exception as e:
        logger.warning(f"Environment checks warning: {e}")
    
    yield
    
    # Shutdown logic
    logger.info("Shutting down application...")


app = FastAPI(
    title="AI-Powered Resume Analyzer",
    description="AI-powered HR platform with resume analysis, ATS scoring, and skill gap analysis",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Register global error handling middleware
app.middleware('http')(error_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint to verify the API is working"""
    return {
        "message": "AI-Powered Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify database connectivity"""
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "disconnected", "detail": str(e)}


# Include application routers
routers = get_all_routers()
for router in routers:
    try:
        app.include_router(router)
        logger.info(f"Included router: {router.prefix}")
    except Exception as e:
        logger.error(f"Error including router: {e}")

# Set up custom OpenAPI schema
app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
