import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from enums.enums import ResponseCodeEnum

from .conftest import TEST_USER

INVALID_DATA = {**TEST_USER, "password": "INVALID PASSWORD"}


@pytest.mark.asyncio
class TestAuthRoutes:
    async def test_register_success(self, client: AsyncClient):
        """Тест успешной регистрации"""
        response = await client.post("/auth/register", json=TEST_USER)
        assert response.status_code == HTTP_201_CREATED
        data = response.json()
        assert data["code"] == ResponseCodeEnum.SUCCESS
        assert data["data"]["email"] == TEST_USER.get("email")
        assert "id" in data["data"]

    async def test_register_duplicate(self, client: AsyncClient):
        """Тест регистрации с уже существующим email"""
        response = await client.post("/auth/register", json=TEST_USER)
        assert response.status_code == HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["code"] == ResponseCodeEnum.USER_ALREADY_EXISTS

    async def test_login_success(self, client: AsyncClient):
        """Тест успешного логина"""
        response = await client.post("/auth/login", json=TEST_USER)
        assert response.status_code == HTTP_200_OK
        data = response.json()
        token = data["data"]["access_token"]
        assert data["code"] == ResponseCodeEnum.SUCCESS
        assert isinstance(token, str)
        assert len(token) > 0

    async def test_login_invalid_password(self, client: AsyncClient):
        """Тест логина с неверным паролем"""
        response = await client.post("/auth/login", json=INVALID_DATA)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        data = response.json()
        assert data["code"] == ResponseCodeEnum.AUTHENTICATION_ERROR
