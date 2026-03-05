from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from src.models.vehicle import Vehicle
from src.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:
    """
    A self-contained repository for all vehicle-related database operations.
    """

    async def get(self, session: AsyncSession, obj_id: UUID) -> Optional[Vehicle]:
        """Get a single vehicle by ID."""
        return await session.get(Vehicle, obj_id)

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Vehicle]:
        """Get multiple vehicles with pagination."""
        query = select(Vehicle).offset(skip).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, *, obj_in: VehicleCreate) -> Vehicle:
        """Create a new vehicle."""
        db_obj = Vehicle.model_validate(obj_in)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, *, db_obj: Vehicle, obj_in: VehicleUpdate
    ) -> Vehicle:
        """Update an existing vehicle."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, db_obj: Vehicle) -> None:
        """Delete a vehicle permanently."""
        await session.delete(db_obj)
        await session.flush()

    async def find_by_registration_number(
        self, session: AsyncSession, *, registration_number: str
    ) -> Optional[Vehicle]:
        """Find a vehicle by its unique registration number."""
        query = select(Vehicle).where(
            Vehicle.registration_number == registration_number
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def find_by_vendor_id(
        self, session: AsyncSession, *, vendor_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Vehicle]:
        """Find all vehicles belonging to a specific vendor."""
        query = (
            select(Vehicle)
            .where(Vehicle.vendor_id == vendor_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def search(
        self, session: AsyncSession, *, term: str, skip: int, limit: int
    ) -> List[Vehicle]:
        """Search for vehicles by make, model, status, or registration number."""
        search_pattern = f"%{term}%"
        query = (
            select(Vehicle)
            .where(
                or_(
                    col(Vehicle.registration_number).ilike(search_pattern),
                    col(Vehicle.make).ilike(search_pattern),
                    col(Vehicle.model).ilike(search_pattern),
                    col(Vehicle.status).ilike(search_pattern),
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())


vehicle_repo = VehicleRepository()
