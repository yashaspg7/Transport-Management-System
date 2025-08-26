from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from src.models.vendor import Vendor
from src.schemas.vendor import VendorCreate, VendorUpdate


class VendorRepository:
    """
    A self-contained repository for all vendor-related database operations.
    """

    async def get(self, session: AsyncSession, obj_id: UUID) -> Optional[Vendor]:
        """Get a single vendor by ID."""
        return await session.get(Vendor, obj_id)

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Vendor]:
        """Get multiple vendors with pagination."""
        query = select(Vendor).offset(skip).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, *, obj_in: VendorCreate) -> Vendor:
        """Create a new vendor."""
        db_obj = Vendor.model_validate(obj_in)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, *, db_obj: Vendor, obj_in: VendorUpdate
    ) -> Vendor:
        """Update an existing vendor."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, db_obj: Vendor) -> None:
        """Delete a vendor."""
        await session.delete(db_obj)
        await session.flush()

    async def find_by_email(
        self, session: AsyncSession, *, email: str
    ) -> Optional[Vendor]:
        """Find a vendor by email."""
        return await self._find_by_unique_fields(session, email=email)

    async def find_by_phone(
        self, session: AsyncSession, *, phone: str
    ) -> Optional[Vendor]:
        """Find a vendor by phone number."""
        return await self._find_by_unique_fields(session, phone=phone)

    async def _find_by_unique_fields(
        self,
        session: AsyncSession,
        *,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[Vendor]:
        """Private helper to find a vendor by any unique field."""
        conditions = []
        if email:
            conditions.append(Vendor.email == email)
        if phone:
            conditions.append(Vendor.phone_number == phone)

        if not conditions:
            return None

        query = select(Vendor).where(or_(*conditions))
        result = await session.execute(query)
        return result.scalars().first()

    async def get_active_count(self, session: AsyncSession) -> int:
        """Gets the count of active vendors."""
        query = select(func.count(col(Vendor.id))).where(Vendor.is_active)
        result = await session.execute(query)
        return result.scalar_one()

    async def search(
        self, session: AsyncSession, *, term: str, skip: int, limit: int
    ) -> List[Vendor]:
        """Search for vendors by a search term."""
        search_pattern = f"%{term}%"
        query = (
            select(Vendor)
            .where(
                or_(
                    col(Vendor.company_name).ilike(search_pattern),
                    col(Vendor.contact_person).ilike(search_pattern),
                    col(Vendor.email).ilike(search_pattern),
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())


vendor_repo = VendorRepository()
