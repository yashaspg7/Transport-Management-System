"""
Dependency injection system for the TMS API.

This module provides dependency functions for injecting services and database sessions
into API endpoints. It follows a simple, maintainable pattern that's easy to understand.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db_session
from src.repositories.vendor import VendorRepository
from src.services.vendor_service import VendorService

# Create a single, reusable instance of the repository
vendor_repo = VendorRepository()


def get_vendor_service() -> VendorService:
    """Dependency to provide the VendorService instance."""
    return VendorService(vendor_repo)


# Type hint for dependencies for cleaner endpoint signatures
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
VendorServiceDep = Annotated[VendorService, Depends(get_vendor_service)]

# Add more service dependencies here as you create new services
# Example:
# async def get_customer_service(
#     session: AsyncSession = Depends(get_db_session)
# ) -> CustomerService:
#     return CustomerService(session)
