from fastapi import APIRouter

from src.core.config import settings

router = APIRouter()


@router.get("/", tags=["Root"])
def read_root():
    return {
        "status": "ok",
        "message": "Welcome to the Transport Management System",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs",
    }


@router.get("/health", tags=["Health Check"])
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }
