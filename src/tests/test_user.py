import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from enums.enums import ResponseCodeEnum

from .conftest import TEST_USER

HEADERS = {"Authorization": ""}
ENDPOINT_URL = "/user/me"
INVALID_TOKEN = "terertert"


@pytest.mark.asyncio
class TestUser:
    async def _get_token(self, user: dict[str, str], client: AsyncClient):
        response = await client.post("/auth/login", json=user)
        data = response.json()
        return data["data"]["access_token"]

    async def test_me_success(self, client: AsyncClient):
        """Тестирование получения информации о пользователе"""
        token = await self._get_token(TEST_USER, client)
        HEADERS["Authorization"] = f"Bearer {token}"
        response = await client.get(ENDPOINT_URL, headers=HEADERS)
        assert response.status_code == HTTP_200_OK
        data = response.json()
        assert data["code"] == ResponseCodeEnum.SUCCESS
        assert data["data"]["email"] == TEST_USER.get("email")

    async def test_me_token(self, client: AsyncClient):
        token = await self._get_token(TEST_USER, client)
        HEADERS["Authorization"] = token
        response = await client.get(ENDPOINT_URL, headers=HEADERS)
        data = response.json()
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert data["code"] == ResponseCodeEnum.UNAUTHORIZED_EXCEPTION
