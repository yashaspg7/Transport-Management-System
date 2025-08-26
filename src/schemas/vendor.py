from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.utils.sanitizers import SanitizationMixin


class VendorBase(BaseModel, SanitizationMixin):
    company_name: str = Field(min_length=1, max_length=255)
    contact_person: Optional[str] = Field(default=None, max_length=255)
    email: EmailStr
    phone_number: Optional[str] = Field(default=None, max_length=20)
    is_active: bool = True


class VendorCreate(VendorBase, SanitizationMixin):
    pass


class VendorUpdate(BaseModel, SanitizationMixin):
    company_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    contact_person: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=20)
    is_active: Optional[bool] = None


class VendorRead(VendorBase, SanitizationMixin):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
