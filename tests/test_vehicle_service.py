from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.schemas.vehicle import VehicleCreate
from src.services.vehicle_service import (
    RegistrationAlreadyExists,
    VehicleService,
    VendorNotFound,
)


# --- Test Data Setup ---
@pytest.fixture
def mock_vendor_repo():
    return AsyncMock()


@pytest.fixture
def mock_vehicle_repo():
    return AsyncMock()


@pytest.fixture
def vehicle_service(mock_vehicle_repo, mock_vendor_repo):
    return VehicleService(vehicle_repo=mock_vehicle_repo, vendor_repo=mock_vendor_repo)


@pytest.fixture
def dummy_vendor_id():
    return uuid4()


@pytest.fixture
def valid_vehicle_create(dummy_vendor_id):
    return VehicleCreate(
        vendor_id=dummy_vendor_id,
        registration_number="KA-01-AB-1234",
        make="Tata",
        model="Prima",
        capacity=15.0,
        status="Active",
    )


# --- Tests ---


@pytest.mark.asyncio
async def test_create_vehicle_success(
    vehicle_service,
    mock_vendor_repo,
    mock_vehicle_repo,
    valid_vehicle_create,
    dummy_vendor_id,
):
    """Test successful vehicle creation when vendor exists and registration is unique."""
    # 1. Setup mocks: Pretend vendor exists, and vehicle does NOT exist
    mock_vendor_repo.get.return_value = AsyncMock(id=dummy_vendor_id)
    mock_vehicle_repo.find_by_registration_number.return_value = None
    mock_vehicle_repo.create.return_value = AsyncMock(
        id=uuid4(), **valid_vehicle_create.model_dump()
    )

    # 2. Execute
    dummy_session = AsyncMock()
    result = await vehicle_service.create_vehicle(dummy_session, valid_vehicle_create)

    # 3. Assert
    assert result.registration_number == valid_vehicle_create.registration_number
    mock_vendor_repo.get.assert_called_once_with(dummy_session, dummy_vendor_id)
    mock_vehicle_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_vehicle_vendor_not_found(
    vehicle_service, mock_vendor_repo, valid_vehicle_create, dummy_vendor_id
):
    """Test that creating a vehicle fails if the vendor ID does not exist."""
    # 1. Setup mock: Pretend vendor is NOT found
    mock_vendor_repo.get.return_value = None

    # 2. Execute & Assert
    dummy_session = AsyncMock()
    with pytest.raises(VendorNotFound) as exc_info:
        await vehicle_service.create_vehicle(dummy_session, valid_vehicle_create)

    assert str(dummy_vendor_id) in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_vehicle_duplicate_registration(
    vehicle_service,
    mock_vendor_repo,
    mock_vehicle_repo,
    valid_vehicle_create,
    dummy_vendor_id,
):
    """Test that creating a vehicle fails if the registration number is already taken."""
    # 1. Setup mocks: Pretend vendor exists, but vehicle ALSO already exists
    mock_vendor_repo.get.return_value = AsyncMock(id=dummy_vendor_id)
    mock_vehicle_repo.find_by_registration_number.return_value = AsyncMock(id=uuid4())

    # 2. Execute & Assert
    dummy_session = AsyncMock()
    with pytest.raises(RegistrationAlreadyExists):
        await vehicle_service.create_vehicle(dummy_session, valid_vehicle_create)
