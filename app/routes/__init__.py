"""
Routes package - API endpoints
"""
from typing import List
from fastapi import APIRouter
import os
import importlib
import logging

logger = logging.getLogger(__name__)


def get_all_routers() -> List[APIRouter]:
    """
    Dynamically discover and load all routers from this package
    """
    routers: List[APIRouter] = []
    routes_dir = os.path.dirname(__file__)
    
    # Import core routers
    try:
        from app.routes import health
        if hasattr(health, 'router'):
            routers.append(health.router)
            logger.info("Loaded health router")
    except ImportError as e:
        logger.warning(f"Could not load health router: {e}")
    
    try:
        from app.routes import auth
        if hasattr(auth, 'router'):
            routers.append(auth.router)
            logger.info("Loaded auth router")
    except ImportError as e:
        logger.warning(f"Could not load auth router: {e}")
    
    return routers
