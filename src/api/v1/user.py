from fastapi import APIRouter, HTTPException, status

from src.api.deps import DBSession, UserServiceDep
from src.models.user import User
from src.schemas.user import UserCreate, UserRead
from src.services.user_services import EmailAlreadyExists, UsernameAlreadyExists

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    session: DBSession,
    service: UserServiceDep,
) -> User:
    """
    Register a new user in the system.

    Args:
        user_in:  The registration payload (name, username, email, password).
        session:  The database session dependency.
        service:  The user service dependency.

    Returns:
        The newly created user object.

    Raises:
        409: If a user with the given email or username already exists.
    """
    try:
        return await service.register(session, user_data=user_in)
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username already exists.",
        )


# add POST /login here
