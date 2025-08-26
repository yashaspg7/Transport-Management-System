import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_root_endpoint(client: AsyncClient):
    """Test the root endpoint returns a successful response."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


async def test_health_endpoint(client: AsyncClient):
    """Test the health check endpoint returns a healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


async def test_root_redirect(client: AsyncClient):
    """
    Tests that the root endpoint '/' redirects to '/docs'.
    """
    response = await client.get("/", follow_redirects=True)
    assert response.status_code == 200
