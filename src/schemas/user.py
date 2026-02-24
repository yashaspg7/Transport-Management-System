from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field
from pydantic import EmailStr, BaseModel, ConfigDict
from src.utils.sanitizers import SanitizationMixin
from pydantic import BaseModel


class UserBase(BaseModel, SanitizationMixin):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str 

class UserCreate(UserBase, SanitizationMixin):
    pass

class UserUpdate(BaseModel, SanitizationMixin):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: Optional[str] = Field(index=True, unique=True)
    username: Optional[str] = Field(index=True, unique=True)
    email: Optional[EmailStr] = Field(index=True, unique=True)

class UserRead(UserBase, SanitizationMixin):
    id: UUID
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)
    