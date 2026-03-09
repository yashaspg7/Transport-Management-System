from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.utils.sanitizers import SanitizationMixin


class VehicleStatus(str, Enum):
    IDLE = "Idle"
    IN_TRANSIT = "In Transit"
    MAINTENANCE = "Maintenance"
    OUT_OF_SERVICE = "Out of Service"


class VehicleBase(BaseModel, SanitizationMixin):
    vendor_id: UUID
    registration_number: str = Field(min_length=1, max_length=50)
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    capacity: float = Field(default=0.0, ge=0.0)
    status: str = Field(default="Active", max_length=50)
    is_active: bool = True


class VehicleCreate(VehicleBase, SanitizationMixin):
    pass


class VehicleUpdate(BaseModel, SanitizationMixin):
    vendor_id: Optional[UUID] = None
    registration_number: Optional[str] = Field(
        default=None, min_length=1, max_length=50
    )
    make: Optional[str] = Field(default=None, min_length=1, max_length=100)
    model: Optional[str] = Field(default=None, min_length=1, max_length=100)
    capacity: Optional[float] = Field(default=None, ge=0.0)
    status: Optional[VehicleStatus] = None
    is_active: Optional[bool] = None


class VehicleRead(VehicleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
