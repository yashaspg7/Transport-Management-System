from typing import List
from uuid import UUID

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.vendor import Vendor
from src.repositories.vendor import VendorRepository
from src.schemas.vendor import VendorCreate, VendorUpdate


class VendorServiceError(Exception):
    """Base exception for the service layer."""

    pass


class VendorNotFound(VendorServiceError):
    """Raised when a vendor is not found."""

    pass


class EmailAlreadyExists(VendorServiceError):
    """Raised when an email already exists."""

    pass


class PhoneAlreadyExists(VendorServiceError):
    """Raised when a phone number already exists."""

    pass


class InvalidEmailFormat(VendorServiceError):
    """Raised when an email format is invalid."""

    pass


class VendorService:
    def __init__(self, vendor_repo: VendorRepository):
        """
        Initializes the service with a vendor repository.

        Args:
            vendor_repo: An instance of VendorRepository for data access.
        """
        self.repo = vendor_repo

    async def create_vendor(
        self, session: AsyncSession, vendor_data: VendorCreate
    ) -> Vendor:
        """
        Creates a new vendor after validating business rules.

        Args:
            session: The database session.
            vendor_data: The data for the new vendor.

        Returns:
            The newly created Vendor object.
        """
        self._validate_email_format(vendor_data.email)

        if await self.repo.find_by_email(session, email=vendor_data.email):
            raise EmailAlreadyExists("A vendor with this email already exists.")

        if vendor_data.phone_number and await self.repo.find_by_phone(
            session, phone=vendor_data.phone_number
        ):
            raise PhoneAlreadyExists("A vendor with this phone number already exists.")

        return await self.repo.create(session, obj_in=vendor_data)

    async def get_vendor_by_id(self, session: AsyncSession, vendor_id: UUID) -> Vendor:
        """
        Retrieves a vendor by its ID, raising an error if not found.

        Args:
            session: The database session.
            vendor_id: The ID of the vendor to retrieve.

        Returns:
            The Vendor object.
        """
        vendor = await self.repo.get(session, vendor_id)
        if not vendor:
            raise VendorNotFound(f"Vendor with ID {vendor_id} not found.")
        return vendor

    async def get_vendor_by_email(self, session: AsyncSession, email: str) -> Vendor:
        """
        Retrieves a vendor by its email, raising an error if not found.

        Args:
            session: The database session.
            email: The email of the vendor to retrieve.

        Returns:
            The Vendor object.
        """
        vendor = await self.repo.find_by_email(session, email=email)
        if not vendor:
            raise VendorNotFound(f"Vendor with email {email} not found.")
        return vendor

    async def get_vendor_by_phone(
        self, session: AsyncSession, phone_number: str
    ) -> Vendor:
        """
        Retrieves a vendor by its phone number, raising an error if not found.

        Args:
            session: The database session.
            phone_number: The phone number of the vendor to retrieve.

        Returns:
            The Vendor object.
        """
        vendor = await self.repo.find_by_phone(session, phone=phone_number)
        if not vendor:
            raise VendorNotFound(f"Vendor with phone number {phone_number} not found.")
        return vendor

    async def get_all_vendors(
        self, session: AsyncSession, skip: int, limit: int
    ) -> List[Vendor]:
        """
        Retrieves a paginated list of all vendors.

        Args:
            session: The database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of Vendor objects.
        """
        return await self.repo.get_multi(session, skip=skip, limit=limit)

    async def update_vendor(
        self, session: AsyncSession, vendor_id: UUID, vendor_data: VendorUpdate
    ) -> Vendor:
        """
        Updates an existing vendor after validating business rules.

        Args:
            session: The database session.
            vendor_id: The ID of the vendor to update.
            vendor_data: The new data for the vendor.

        Returns:
            The updated Vendor object.
        """
        db_vendor = await self.get_vendor_by_id(session, vendor_id)
        update_data = vendor_data.model_dump(exclude_unset=True)

        # Check email uniqueness
        if "email" in update_data and update_data["email"] != db_vendor.email:
            self._validate_email_format(update_data["email"])
            existing_vendor = await self.repo.find_by_email(
                session, email=update_data["email"]
            )
            if existing_vendor and existing_vendor.id != vendor_id:
                raise EmailAlreadyExists("A vendor with this email already exists.")

        # Check phone number uniqueness
        if (
            "phone_number" in update_data
            and update_data["phone_number"] != db_vendor.phone_number
        ):
            existing_vendor = await self.repo.find_by_phone(
                session, phone=update_data["phone_number"]
            )
            if existing_vendor and existing_vendor.id != vendor_id:
                raise PhoneAlreadyExists(
                    "A vendor with this phone number already exists."
                )

        return await self.repo.update(session, db_obj=db_vendor, obj_in=vendor_data)

    async def delete_vendor(
        self, session: AsyncSession, vendor_id: UUID, permanent: bool = False
    ) -> None:
        """
        Deletes a vendor, either permanently or by marking it as inactive (soft delete).

        Args:
            session: The database session.
            vendor_id: The ID of the vendor to delete.
            permanent: If True, the vendor is permanently deleted from the database.
        """
        db_vendor = await self.get_vendor_by_id(session, vendor_id)
        if permanent:
            await self.repo.delete(session, db_obj=db_vendor)
        else:
            soft_delete_update = VendorUpdate(is_active=False)
            await self.repo.update(session, db_obj=db_vendor, obj_in=soft_delete_update)

    async def get_active_vendors_count(self, session: AsyncSession) -> int:
        """
        Gets the count of active vendors.

        Args:
            session: The database session.

        Returns:
            The total number of active vendors.
        """
        return await self.repo.get_active_count(session)

    async def search_vendors(
        self, session: AsyncSession, term: str, skip: int, limit: int
    ) -> List[Vendor]:
        """
        Searches for vendors by a term across multiple fields.

        Args:
            session: The database session.
            term: The search term.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of vendors matching the search term.
        """
        if not term:
            return []

        return await self.repo.search(session, term=term, skip=skip, limit=limit)

    def _validate_email_format(self, email: str) -> None:
        """Private helper to validate email format."""
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise InvalidEmailFormat("Invalid email format.")
