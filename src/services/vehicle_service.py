from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.vehicle import Vehicle
from src.repositories.vehicle import VehicleRepository
from src.repositories.vendor import VendorRepository
from src.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleServiceError(Exception):
    """Base exception for the vehicle service layer."""

    pass


class VehicleNotFound(VehicleServiceError):
    pass


class RegistrationAlreadyExists(VehicleServiceError):
    pass


class VendorNotFound(VehicleServiceError):
    pass


class VehicleService:
    def __init__(self, vehicle_repo: VehicleRepository, vendor_repo: VendorRepository):
        self.repo = vehicle_repo
        self.vendor_repo = vendor_repo

    async def create_vehicle(
        self, session: AsyncSession, vehicle_data: VehicleCreate
    ) -> Vehicle:
        # 1. Validate that the vendor exists
        vendor = await self.vendor_repo.get(session, vehicle_data.vendor_id)
        if not vendor:
            raise VendorNotFound(f"Vendor with ID {vehicle_data.vendor_id} not found.")

        # 2. Validate registration uniqueness
        existing_vehicle = await self.repo.find_by_registration_number(
            session, registration_number=vehicle_data.registration_number
        )
        if existing_vehicle:
            raise RegistrationAlreadyExists(
                "A vehicle with this registration number already exists."
            )

        return await self.repo.create(session, obj_in=vehicle_data)

    async def get_vehicle_by_id(
        self, session: AsyncSession, vehicle_id: UUID
    ) -> Vehicle:
        vehicle = await self.repo.get(session, vehicle_id)
        if not vehicle:
            raise VehicleNotFound(f"Vehicle with ID {vehicle_id} not found.")
        return vehicle

    async def get_vehicle_by_registration(
        self, session: AsyncSession, registration_number: str
    ) -> Vehicle:
        vehicle = await self.repo.find_by_registration_number(
            session, registration_number=registration_number
        )
        if not vehicle:
            raise VehicleNotFound(
                f"Vehicle with registration {registration_number} not found."
            )
        return vehicle

    async def get_all_vehicles(
        self, session: AsyncSession, skip: int, limit: int
    ) -> List[Vehicle]:
        return await self.repo.get_multi(session, skip=skip, limit=limit)

    async def get_vehicles_by_vendor(
        self, session: AsyncSession, vendor_id: UUID, skip: int, limit: int
    ) -> List[Vehicle]:
        """Fetch vehicles for specific vendor, ensuring vendor exists first."""

        vendor = await self.vendor_repo.get(session, vendor_id)
        if not vendor:
            raise VendorNotFound(f"Vendor with ID {vendor_id} not found.")

        return await self.repo.find_by_vendor_id(
            session, vendor_id=vendor_id, skip=skip, limit=limit
        )

    async def update_vehicle(
        self, session: AsyncSession, vehicle_id: UUID, vehicle_data: VehicleUpdate
    ) -> Vehicle:
        db_vehicle = await self.get_vehicle_by_id(session, vehicle_id)
        update_data = vehicle_data.model_dump(exclude_unset=True)

        # Check if they are trying to change the vendor, and validate the new vendor exists
        if (
            "vendor_id" in update_data
            and update_data["vendor_id"] != db_vehicle.vendor_id
        ):
            vendor = await self.vendor_repo.get(session, update_data["vendor_id"])
            if not vendor:
                raise VendorNotFound(
                    f"Vendor with ID {update_data['vendor_id']} not found."
                )

        # Check registration uniqueness if it's being updated
        if (
            "registration_number" in update_data
            and update_data["registration_number"] != db_vehicle.registration_number
        ):
            existing_vehicle = await self.repo.find_by_registration_number(
                session, registration_number=update_data["registration_number"]
            )
            if existing_vehicle and existing_vehicle.id != vehicle_id:
                raise RegistrationAlreadyExists(
                    "A vehicle with this registration number already exists."
                )

        return await self.repo.update(session, db_obj=db_vehicle, obj_in=vehicle_data)

    async def delete_vehicle(
        self, session: AsyncSession, vehicle_id: UUID, permanent: bool = False
    ) -> None:
        db_vehicle = await self.get_vehicle_by_id(session, vehicle_id)
        if permanent:
            await self.repo.delete(session, db_obj=db_vehicle)
        else:
            # Soft delete logic
            soft_delete_update = VehicleUpdate(is_active=False)
            await self.repo.update(
                session, db_obj=db_vehicle, obj_in=soft_delete_update
            )

    async def search_vehicles(
        self, session: AsyncSession, term: str, skip: int, limit: int
    ) -> List[Vehicle]:
        if not term:
            return []
        return await self.repo.search(session, term=term, skip=skip, limit=limit)
