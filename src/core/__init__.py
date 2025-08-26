"""
Core Package

This package contains the fundamental components of the Transport Management System:
- Configuration management
- Database connection and session handling
- Logging setup
- Security utilities

The core package provides the foundation that all other parts of the application depend on.

Key Components:
- settings: Application configuration and environment variables
- engine: Database engine for async operations
- get_db_session: Database session dependency for FastAPI
- get_naive_utc_now: Utility for consistent timestamp generation

Usage:
    from src.core.config import settings
    from src.core.db import engine, get_db_session
"""

from .config import settings
from .db import engine, get_db_session, get_naive_utc_now

__all__ = [
    # Configuration
    "settings",
    # Database
    "engine",
    "get_db_session",
    "get_naive_utc_now",
]

# Version info
__version__ = "0.1.0"
