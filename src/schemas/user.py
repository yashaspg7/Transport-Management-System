from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field

from src.utils.sanitizers import SanitizationMixin


class UserBase(BaseModel, SanitizationMixin):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=254)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserUpdate(BaseModel, SanitizationMixin):
    name: Optional[str] = Field(min_length=1, max_length=100)
    username: Optional[str] = Field(min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(min_length=1, max_length=100)


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
