from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.schemas.vehicle import VehicleCreate, VehicleStatus, VehicleUpdate
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
        status=VehicleStatus.IDLE,
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


# --- Update Vehicle Tests ---


@pytest.mark.asyncio
async def test_update_vehicle_success(vehicle_service, mock_vehicle_repo):
    """Test updating a vehicle without triggering validation errors."""
    dummy_session = AsyncMock()
    vehicle_id = uuid4()

    # Mock the existing vehicle in the DB
    existing_vehicle = AsyncMock(
        id=vehicle_id, vendor_id=uuid4(), registration_number="OLD-123"
    )
    mock_vehicle_repo.get.return_value = existing_vehicle

    # Execute
    update_data = VehicleUpdate(make="Toyota")
    await vehicle_service.update_vehicle(dummy_session, vehicle_id, update_data)

    # Assert
    mock_vehicle_repo.get.assert_called_once_with(dummy_session, vehicle_id)
    mock_vehicle_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_vehicle_vendor_not_found(
    vehicle_service, mock_vehicle_repo, mock_vendor_repo
):
    """Test updating a vehicle fails if the new vendor does not exist."""
    dummy_session = AsyncMock()
    vehicle_id = uuid4()

    existing_vehicle = AsyncMock(
        id=vehicle_id, vendor_id=uuid4(), registration_number="OLD-123"
    )
    mock_vehicle_repo.get.return_value = existing_vehicle

    # Mock the new vendor failing to be found
    mock_vendor_repo.get.return_value = None
    new_vendor_id = uuid4()
    update_data = VehicleUpdate(vendor_id=new_vendor_id)

    with pytest.raises(VendorNotFound):
        await vehicle_service.update_vehicle(dummy_session, vehicle_id, update_data)


@pytest.mark.asyncio
async def test_update_vehicle_duplicate_registration(
    vehicle_service, mock_vehicle_repo
):
    """Test updating a vehicle fails if the new registration number is taken."""
    dummy_session = AsyncMock()
    vehicle_id = uuid4()

    existing_vehicle = AsyncMock(
        id=vehicle_id, vendor_id=uuid4(), registration_number="OLD-123"
    )
    mock_vehicle_repo.get.return_value = existing_vehicle

    # Mock finding a DIFFERENT vehicle with the requested new registration
    other_vehicle = AsyncMock(id=uuid4(), registration_number="NEW-123")
    mock_vehicle_repo.find_by_registration_number.return_value = other_vehicle

    update_data = VehicleUpdate(registration_number="NEW-123")

    with pytest.raises(RegistrationAlreadyExists):
        await vehicle_service.update_vehicle(dummy_session, vehicle_id, update_data)


# --- Delete Vehicle Tests ---


@pytest.mark.asyncio
async def test_delete_vehicle_soft(vehicle_service, mock_vehicle_repo):
    """Test soft deletion passes is_active=False to the update repo method."""
    dummy_session = AsyncMock()
    vehicle_id = uuid4()

    existing_vehicle = AsyncMock(id=vehicle_id, is_active=True)
    mock_vehicle_repo.get.return_value = existing_vehicle

    # Execute soft delete
    await vehicle_service.delete_vehicle(dummy_session, vehicle_id, permanent=False)

    # Assert delete was NOT called, but update WAS called
    mock_vehicle_repo.delete.assert_not_called()
    mock_vehicle_repo.update.assert_called_once()

    # Assert the data passed to update sets is_active to False
    called_args = mock_vehicle_repo.update.call_args.kwargs
    assert called_args["obj_in"].is_active is False


@pytest.mark.asyncio
async def test_delete_vehicle_permanent(vehicle_service, mock_vehicle_repo):
    """Test permanent deletion calls the repo delete method directly."""
    dummy_session = AsyncMock()
    vehicle_id = uuid4()

    existing_vehicle = AsyncMock(id=vehicle_id, is_active=True)
    mock_vehicle_repo.get.return_value = existing_vehicle

    # Execute permanent delete
    await vehicle_service.delete_vehicle(dummy_session, vehicle_id, permanent=True)

    # Assert update was NOT called, but delete WAS called
    mock_vehicle_repo.update.assert_not_called()
    mock_vehicle_repo.delete.assert_called_once_with(
        dummy_session, db_obj=existing_vehicle
    )
