import pytest
from httpx import AsyncClient, ASGITransport

from ..main import app
from ..schemas.outgoing import User
from .mocks import test_bet_simple


@pytest.mark.asyncio(loop_scope="session")
async def test_create_bet_without_user(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            url="/bet",
            json=test_bet_simple
        )
        assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_create_bet_with_user(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_response = await ac.post(url="/user")
        bet_response = await ac.post(
            url="/bet",
            json=test_bet_simple
        )
        assert user_response.status_code == 201
        # assert bet_response.status_code == 201
        # assert User.model_validate(user_response.json())
