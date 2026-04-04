import asyncio
import os
from typing import AsyncGenerator
from uuid import UUID

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.db import get_db_session
from src.core.security import create_access_token
from src.main import app
from src.models.user import User
from src.models.vendor import SQLModel

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/testdb"
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates a new event loop for the entire test session, ensuring a clean
    asyncio environment.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """
    Session-scoped fixture to create and drop all database tables.
    'autouse=True' ensures this runs automatically for the session.
    """
    async_engine = create_async_engine(TEST_DATABASE_URL)
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a transactional database session for each test function.[2]
    This is the cornerstone of test isolation. It creates a transaction,
    yields a session, and rolls back the transaction after the test,
    undoing any changes.[3, 4]
    """
    async_engine = create_async_engine(TEST_DATABASE_URL)
    async with async_engine.connect() as conn:
        await conn.begin()
        async_session_factory = async_sessionmaker(conn, expire_on_commit=False)
        async with async_session_factory() as session:
            yield session
        await conn.rollback()
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides a configured httpx.AsyncClient for making API requests.
    Overrides BOTH the database session AND the authentication.
    """

    # Override the Database Session (Connect to Test DB)
    def override_get_db_session() -> AsyncSession:
        return db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    # Clean up overrides after the test
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def authorized_client(
    client: AsyncClient, db_session: AsyncSession
) -> AsyncClient:
    """
    Creates a valid user in the test DB and attaches a real JWT token
    to the client headers for testing protected routes.
    """
    user_id = UUID("00000000-0000-0000-0000-000000000000")

    # 1. Put the test user in the test database
    test_user = User(
        id=user_id,
        email="test@example.com",
        username="testuser",
        hashed_password="fake",
        name="Test User",
        is_active=True,
    )
    db_session.add(test_user)
    await db_session.flush()  # Make it available to the session

    # 2. Generate a real token
    access_token = create_access_token(data={"sub": str(user_id)})

    # 3. Attach it to the client headers
    client.headers["Authorization"] = f"Bearer {access_token}"

    return client
