from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from src.api.deps import DBSession, VehicleServiceDep
from src.models.vehicle import Vehicle
from src.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from src.services.vehicle_service import (
    RegistrationAlreadyExists,
    VehicleNotFound,
    VendorNotFound,
)

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    session: DBSession,
    service: VehicleServiceDep,
) -> Vehicle:
    try:
        return await service.create_vehicle(session, vehicle_data=vehicle_in)
    except VendorNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegistrationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[VehicleRead])
async def list_vehicles(
    session: DBSession,
    service: VehicleServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[Vehicle]:
    return await service.get_all_vehicles(session, skip=skip, limit=limit)


@router.get("/search/", response_model=List[VehicleRead])
async def search_vehicles(
    session: DBSession,
    service: VehicleServiceDep,
    q: str = Query(
        "", description="Search term for make, model, status, or registration."
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[Vehicle]:
    return await service.search_vehicles(session, term=q, skip=skip, limit=limit)


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle_by_id(
    vehicle_id: UUID,
    session: DBSession,
    service: VehicleServiceDep,
) -> Vehicle:
    try:
        return await service.get_vehicle_by_id(session, vehicle_id=vehicle_id)
    except VehicleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/vendor/{vendor_id}", response_model=List[VehicleRead])
async def get_vehicles_by_vendor(
    vendor_id: UUID,
    session: DBSession,
    service: VehicleServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[Vehicle]:
    return await service.get_vehicles_by_vendor(
        session, vendor_id=vendor_id, skip=skip, limit=limit
    )


@router.put("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    vehicle_id: UUID,
    vehicle_in: VehicleUpdate,
    session: DBSession,
    service: VehicleServiceDep,
) -> Vehicle:
    try:
        return await service.update_vehicle(
            session, vehicle_id=vehicle_id, vehicle_data=vehicle_in
        )
    except (VehicleNotFound, VendorNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegistrationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: UUID,
    session: DBSession,
    service: VehicleServiceDep,
    permanent: bool = Query(False),
) -> None:
    try:
        await service.delete_vehicle(
            session, vehicle_id=vehicle_id, permanent=permanent
        )
    except VehicleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
