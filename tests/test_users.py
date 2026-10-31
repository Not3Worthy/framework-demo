import pytest
from collections.abc import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from framework_demo.main import app
from framework_demo.database import Base, get_db

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:admin1234@localhost:5432/framework_db"

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        # Clean up tables after test
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.anyio
async def test_list_users():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create a user first
        await ac.post("/users/", json={"username": "alice", "email": "alice@example.com"})
        
        response = await ac.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "alice"