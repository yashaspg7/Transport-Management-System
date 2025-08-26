from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import Field, SQLModel

from src.core.db import get_naive_utc_now


class Vendor(SQLModel, table=True):
    """
    Represents the Vendor table in the database.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    company_name: str = Field(index=True, max_length=255)
    contact_person: Optional[str] = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone_number: Optional[str] = Field(
        default=None, unique=True, index=True, max_length=20
    )

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=get_naive_utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=get_naive_utc_now,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
