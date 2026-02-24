from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field

from src.utils.sanitizers import SanitizationMixin


class UserBase(BaseModel, SanitizationMixin):
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()
    hashed_password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel, SanitizationMixin):
    name: Optional[str] = Field()
    username: Optional[str] = Field()
    email: Optional[EmailStr] = Field()


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
