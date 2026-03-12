from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserUpdate


class UserRepository:
    async def get_by_id(self, session: AsyncSession, obj_id: UUID) -> Optional[User]:
        return await session.get(User, obj_id)

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> Optional[User]:
        result = await session.execute(select(User).where(User.username == username))  # type: ignore[arg-type]
        return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))  # type: ignore[arg-type]
        return result.scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> Sequence[User]:
        result = await session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, session: AsyncSession, db_obj: User) -> User:
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: User, obj_in: UserUpdate
    ) -> User:
        updated_data = obj_in.model_dump(exclude_unset=True)
        for fields, values in updated_data.items():
            setattr(db_obj, fields, values)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, db_obj: User):
        await session.delete(db_obj)
        await session.flush()


user_repo = UserRepository()
