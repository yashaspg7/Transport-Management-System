from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserUpdate


class UserServiceError(Exception):
    """Base exception for the user service layer."""

    pass


class UserNotFound(UserServiceError):
    """Raised when a user is not found."""

    pass


class EmailAlreadyExists(UserServiceError):
    """Raised when a user with the given email already exists."""

    pass


class UsernameAlreadyExists(UserServiceError):
    """Raised when a user with the given username already exists."""

    pass


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def register(self, session: AsyncSession, user_data: UserCreate) -> User:
        if await self.repo.get_by_email(session, email=user_data.email):
            raise EmailAlreadyExists("A user with this email already exists.")

        if await self.repo.get_by_username(session, username=user_data.username):
            raise UsernameAlreadyExists("A user with this username already exists.")

        db_obj = User(
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        return await self.repo.create(session, db_obj=db_obj)

    async def update_user(
        self, session: AsyncSession, user_id: UUID, user_in: UserUpdate
    ) -> User:
        db_user = await self.repo.get_by_id(session, user_id)
        if not db_user:
            raise UserNotFound(f"User with id {user_id} was not found.")
        return await self.repo.update(session, db_obj=db_user, obj_in=user_in)

    async def delete_user(self, session: AsyncSession, user_id: UUID) -> None:
        db_user = await self.repo.get_by_id(session, user_id)
        if not db_user:
            raise UserNotFound(f"User with id {user_id} was not found.")
        await self.repo.delete(session, db_obj=db_user)
