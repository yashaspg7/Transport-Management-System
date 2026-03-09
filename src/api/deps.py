"""
Dependency injection system for the TMS API.

This module provides dependency functions for injecting services and database sessions
into API endpoints. It follows a simple, maintainable pattern that's easy to understand.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db_session
from src.repositories.vehicle import vehicle_repo
from src.repositories.vendor import vendor_repo
from src.services.vehicle_service import VehicleService
from src.services.vendor_service import VendorService

# Create a single, reusable instance of the repository


def get_vendor_service() -> VendorService:
    """Dependency to provide the VendorService instance."""
    return VendorService(vendor_repo)


def get_vehicle_service() -> VehicleService:
    """Dependency to provide the VehicleService instance."""
    return VehicleService(vehicle_repo=vehicle_repo, vendor_repo=vendor_repo)


# Type hint for dependencies for cleaner endpoint signatures
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
VendorServiceDep = Annotated[VendorService, Depends(get_vendor_service)]
VehicleServiceDep = Annotated[VehicleService, Depends(get_vehicle_service)]

# Add more service dependencies here as you create new services
# Example:
# async def get_customer_service(
#     session: AsyncSession = Depends(get_db_session)
# ) -> CustomerService:
#     return CustomerService(session)
