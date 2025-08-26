from typing import List
from uuid import UUID

from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from src.api.deps import DBSession, VendorServiceDep
from src.models.vendor import Vendor
from src.schemas.vendor import VendorCreate, VendorRead, VendorUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])


class VendorCountResponse(BaseModel):
    active_vendors_count: int


@router.post("/", response_model=VendorRead, status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor_in: VendorCreate,
    session: DBSession,
    service: VendorServiceDep,
) -> Vendor:
    """
    Create a new vendor in the system.

    Args:
        vendor_in: The vendor data to create.
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        The newly created vendor object.
    """
    return await service.create_vendor(session, vendor_data=vendor_in)


@router.get("/", response_model=List[VendorRead])
async def list_vendors(
    session: DBSession,
    service: VendorServiceDep,
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination."),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return."
    ),
) -> List[Vendor]:
    """
    Retrieve all vendors with pagination.

    Args:
        session: The database session dependency.
        service: The vendor service dependency.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of vendor objects.
    """
    return await service.get_all_vendors(session, skip=skip, limit=limit)


@router.get("/search/", response_model=List[VendorRead])
async def search_vendors(
    session: DBSession,
    service: VendorServiceDep,
    q: str = Query("", description="Search term for company, contact, or email."),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination."),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return."
    ),
) -> List[Vendor]:
    """
    Search for vendors by a search term across multiple fields.

    Args:
        session: The database session dependency.
        service: The vendor service dependency.
        q: The search term.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of vendors matching the search term.
    """
    return await service.search_vendors(session, term=q, skip=skip, limit=limit)


@router.get("/count", response_model=VendorCountResponse)
async def get_active_vendors_count(
    session: DBSession,
    service: VendorServiceDep,
) -> VendorCountResponse:
    """
    Get the total count of active vendors.

    Args:
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        A dictionary containing the count of active vendors.
    """
    count = await service.get_active_vendors_count(session)
    return VendorCountResponse(active_vendors_count=count)


@router.get("/{vendor_id}", response_model=VendorRead)
async def get_vendor_by_id(
    vendor_id: UUID,
    session: DBSession,
    service: VendorServiceDep,
) -> Vendor:
    """
    Retrieve a specific vendor by their unique ID.

    Args:
        vendor_id: The UUID of the vendor to retrieve.
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        The vendor object.
    """
    return await service.get_vendor_by_id(session, vendor_id=vendor_id)


@router.get("/email/{email}", response_model=VendorRead)
async def get_vendor_by_email(
    email: str,
    session: DBSession,
    service: VendorServiceDep,
) -> Vendor:
    """
    Retrieve a specific vendor by their email address.

    Args:
        email: The email address of the vendor to retrieve.
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        The vendor object.
    """
    return await service.get_vendor_by_email(session, email=email)


@router.get("/phone/{phone_number}", response_model=VendorRead)
async def get_vendor_by_phone(
    phone_number: str,
    session: DBSession,
    service: VendorServiceDep,
) -> Vendor:
    """
    Retrieve a specific vendor by their phone number.

    Args:
        phone_number: The phone number of the vendor to retrieve.
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        The vendor object.
    """
    return await service.get_vendor_by_phone(session, phone_number=phone_number)


@router.put("/{vendor_id}", response_model=VendorRead)
async def update_vendor(
    vendor_id: UUID,
    vendor_in: VendorUpdate,
    session: DBSession,
    service: VendorServiceDep,
) -> Vendor:
    """

    Update a vendor's information.

    Args:
        vendor_id: The UUID of the vendor to update.
        vendor_in: The new data for the vendor.
        session: The database session dependency.
        service: The vendor service dependency.

    Returns:
        The updated vendor object.
    """
    return await service.update_vendor(
        session, vendor_id=vendor_id, vendor_data=vendor_in
    )


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(
    vendor_id: UUID,
    session: DBSession,
    service: VendorServiceDep,
    permanent: bool = Query(False, description="Set to true for permanent deletion."),
) -> None:
    """
    Delete a vendor. By default, this is a soft delete (sets is_active=False).

    Args:
        vendor_id: The UUID of the vendor to delete.
        session: The database session dependency.
        service: The vendor service dependency.
        permanent: If true, the vendor is permanently deleted from the database.
    """
    await service.delete_vendor(session, vendor_id=vendor_id, permanent=permanent)
