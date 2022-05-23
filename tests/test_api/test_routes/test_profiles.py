import pytest
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.db.repositories.users import UsersRepository
from app.models.domain.users import UserInDB
from app.models.schemas.profiles import ProfileInResponse

pytestmark = pytest.mark.asyncio


async def test_unregistered_user_will_receive_profile(
    app: FastAPI, client: AsyncClient, test_user: UserInDB
) -> None:
    response = await client.get(
        app.url_path_for("profiles:get-profile", username=test_user.username)
    )
    profile = ProfileInResponse(**response.json())
    assert profile.profile.username == test_user.username


async def test_user_will_receive_profile(
    app: FastAPI, authorized_client: AsyncClient, pool: Pool
) -> None:
    async with pool.acquire() as conn:
        users_repo = UsersRepository(conn)
        user = await users_repo.create_user(
            username="user_for_following",
            email="test-for-following@email.com",
            password="password",
        )

    response = await authorized_client.get(
        app.url_path_for("profiles:get-profile", username=user.username)
    )
    profile = ProfileInResponse(**response.json())
    assert profile.profile.username == user.username


@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "profiles:get-profile"),),
)
async def test_user_can_not_retrieve_not_existing_profile(
    app: FastAPI, authorized_client: AsyncClient, api_method: str, route_name: str
) -> None:
    response = await authorized_client.request(
        api_method, app.url_path_for(route_name, username="not_existing_user")
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
