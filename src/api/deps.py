"""
Dependency injection system for the TMS API.

This module provides dependency functions for injecting services and database sessions
into API endpoints. It follows a simple, maintainable pattern that's easy to understand.
"""

from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db import get_db_session
from src.models.user import User
from src.repositories.user import UserRepository
from src.repositories.vendor import VendorRepository
from src.services.user_services import UserService
from src.services.vendor_service import VendorService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Create a single, reusable instance of the repository
vendor_repo = VendorRepository()
user_repo = UserRepository()


def get_vendor_service() -> VendorService:
    """Dependency to provide the VendorService instance."""
    return VendorService(vendor_repo)


def get_user_service() -> UserService:
    """Dependency to provide the UserService instance."""
    return UserService(user_repo)


# Type hint for dependencies for cleaner endpoint signatures
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
VendorServiceDep = Annotated[VendorService, Depends(get_vendor_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# Add more service dependencies here as you create new services
# Example:
# async def get_customer_service(
#     session: AsyncSession = Depends(get_db_session)
# ) -> CustomerService:
#     return CustomerService(session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: DBSession,
) -> User:
    """
    Validates the JWT token and returns the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        user_uuid = UUID(user_id_str)

    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = await user_repo.get_by_id(session, user_uuid)
    if user is None:
        raise credentials_exception

    return user


# Type hint for authenticated users
CurrentUser = Annotated[User, Depends(get_current_user)]
