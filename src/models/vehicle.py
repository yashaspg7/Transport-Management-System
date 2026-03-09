from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Field, SQLModel

from src.core.db import get_naive_utc_now


class Vehicle(SQLModel, table=True):
    """
    Represents the Vehicle table in the database.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    vendor_id: UUID = Field(foreign_key="vendor.id", index=True)
    registration_number: str = Field(unique=True, index=True, max_length=50)

    make: str = Field(max_length=100)
    model: str = Field(max_length=100)
    capacity: float = Field(default=0.0, description="Payload capacity in kg/tons")
    status: str = Field(
        default="Idle", max_length=50
    )  # e.g., Idle, In Transit, Maintenance, Out of Service

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=get_naive_utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=get_naive_utc_now,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )
