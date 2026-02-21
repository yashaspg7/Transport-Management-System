import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.vendor import VendorRepository
from src.schemas.vendor import VendorCreate
from src.services.vendor_service import (
    VendorNotFound,
    VendorService,
)

pytestmark = pytest.mark.asyncio


async def test_create_vendor_success(db_session: AsyncSession):
    """Test successful vendor creation at the service level."""
    vendor_repo = VendorRepository()
    vendor_service = VendorService(vendor_repo)

    vendor_data = VendorCreate(company_name="Service Test Co", email="service@test.com")
    new_vendor = await vendor_service.create_vendor(db_session, vendor_data)

    assert new_vendor.company_name == "Service Test Co"
    assert new_vendor.id is not None


async def test_get_vendor_by_id_not_found(db_session: AsyncSession):
    """Test that the service raises VendorNotFound for a non-existent ID."""
    vendor_repo = VendorRepository()
    vendor_service = VendorService(vendor_repo)

    with pytest.raises(VendorNotFound):
        await vendor_service.get_vendor_by_id(db_session, uuid.uuid4())
