import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# FIX: Change 'client' to 'authorized_client'
async def test_create_and_get_vendor_flow(authorized_client: AsyncClient):
    """Test the full CRUD flow for a vendor via the API."""
    # 1. Create
    create_response = await authorized_client.post(
        "/api/v1/vendors/",
        json={"company_name": "Full Flow Inc.", "email": "flow@test.com"},
    )
    assert create_response.status_code == 201
    vendor_data = create_response.json()
    vendor_id = vendor_data["id"]

    # 2. Read
    get_response = await authorized_client.get(f"/api/v1/vendors/{vendor_id}")
    assert get_response.status_code == 200
    assert get_response.json()["company_name"] == "Full Flow Inc."

    # 3. Update
    update_response = await authorized_client.put(
        f"/api/v1/vendors/{vendor_id}",
        json={"company_name": "Full Flow Updated Inc."},
    )
    assert update_response.status_code == 200
    assert update_response.json()["company_name"] == "Full Flow Updated Inc."

    # 4. Delete
    delete_response = await authorized_client.delete(f"/api/v1/vendors/{vendor_id}")
    assert delete_response.status_code == 204

    # 5. Verify Deletion
    final_get_response = await authorized_client.get(f"/api/v1/vendors/{vendor_id}")
    assert final_get_response.status_code == 200
    assert not final_get_response.json()["is_active"]


# FIX: Change 'client' to 'authorized_client'
async def test_create_vendor_conflict(authorized_client: AsyncClient):
    """Test that creating a vendor with a duplicate email returns a 409 Conflict."""
    await authorized_client.post(
        "/api/v1/vendors/",
        json={"company_name": "Conflict Co", "email": "conflict@test.com"},
    )

    response = await authorized_client.post(
        "/api/v1/vendors/",
        json={"company_name": "Another Co", "email": "conflict@test.com"},
    )
    assert response.status_code == 409
    assert "email already exists" in response.json()["detail"]
