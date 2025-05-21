import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app import app

TEST_URL = "http://127.0.0.1:8000/api/v1"
TEST_USER = {"email": "testuser@mail.com", "password": "test123"}


@pytest_asyncio.fixture
async def client() -> TestClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=TEST_URL) as client:
        yield client
