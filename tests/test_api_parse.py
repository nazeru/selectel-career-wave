from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import FastAPI

from app.api.v1 import parse
from app.api.v1.router import api_router

pytestmark = pytest.mark.anyio


@pytest.fixture
def session_sentinel():
    return object()


@pytest.fixture
def parse_app(session_sentinel):
    app = FastAPI()
    app.include_router(api_router)

    async def override_session():
        yield session_sentinel

    app.dependency_overrides[parse.get_session] = override_session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
async def parse_client(parse_app):
    transport = httpx.ASGITransport(app=parse_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_parse_endpoint_returns_created_count(parse_client, session_sentinel):
    with patch(
        "app.api.v1.parse.parse_and_store",
        new=AsyncMock(return_value=7),
    ) as parse_mock:
        response = await parse_client.post("/api/v1/parse/")

    assert response.status_code == 200
    assert response.json() == {"created": 7}
    parse_mock.assert_awaited_once_with(session_sentinel)


async def test_parse_endpoint_returns_500_when_service_raises(parse_app):
    transport = httpx.ASGITransport(app=parse_app, raise_app_exceptions=False)
    with patch(
        "app.api.v1.parse.parse_and_store",
        new=AsyncMock(side_effect=RuntimeError("boom")),
    ):
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post("/api/v1/parse/")

    assert response.status_code == 500
