from sqlmodel import Field,SQLModel
from typing import Optional
from uuid import UUID, uuid4
from pydantic import EmailStr
from datetime import datetime
from src.core.db import get_naive_utc_now
from sqlalchemy import func

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str 
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=get_naive_utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=get_naive_utc_now, nullable=False,sa_column_kwargs={"onupdate":func.now()})
    