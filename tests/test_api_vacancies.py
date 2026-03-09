from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import FastAPI

from app.api.v1 import vacancies
from app.api.v1.router import api_router

pytestmark = pytest.mark.anyio


@pytest.fixture
def session_sentinel():
    return object()


@pytest.fixture
def vacancies_app(session_sentinel):
    app = FastAPI()
    app.include_router(api_router)

    async def override_session():
        yield session_sentinel

    app.dependency_overrides[vacancies.get_session] = override_session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
async def vacancies_client(vacancies_app):
    transport = httpx.ASGITransport(app=vacancies_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_list_vacancies_returns_payload_and_passes_filters(
    vacancies_client, session_sentinel, vacancy_factory
):
    with patch(
        "app.api.v1.vacancies.list_vacancies",
        new=AsyncMock(return_value=[vacancy_factory()]),
    ) as list_mock:
        response = await vacancies_client.get(
            "/api/v1/vacancies/",
            params={"city": "mos", "timetable_mode_name": "remote"},
        )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Python Developer"
    called_session, called_timetable, called_city = list_mock.await_args.args
    assert called_session is session_sentinel
    assert called_timetable == "remote"
    assert called_city == "mos"


@pytest.mark.parametrize("endpoint", ["/api/v1/vacancies/1", "/api/v1/vacancies/999"])
async def test_get_vacancy_returns_404_when_missing(vacancies_client, endpoint):
    with patch("app.api.v1.vacancies.get_vacancy", new=AsyncMock(return_value=None)):
        response = await vacancies_client.get(endpoint)

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


@pytest.mark.parametrize(
    ("method", "url"),
    [
        ("get", "/api/v1/vacancies/0"),
        ("get", "/api/v1/vacancies/2147483648"),
        ("put", "/api/v1/vacancies/0"),
        ("put", "/api/v1/vacancies/2147483648"),
        ("delete", "/api/v1/vacancies/0"),
        ("delete", "/api/v1/vacancies/2147483648"),
    ],
)
async def test_vacancy_id_out_of_range_returns_422(
    vacancies_client, vacancy_payload_factory, method, url
):
    if method == "put":
        response = await vacancies_client.put(url, json=vacancy_payload_factory())
    else:
        response = await getattr(vacancies_client, method)(url)

    assert response.status_code == 422


async def test_create_vacancy_returns_409_on_external_id_conflict(
    vacancies_client, vacancy_payload_factory, vacancy_factory
):
    with patch(
        "app.api.v1.vacancies.get_vacancy_by_external_id",
        new=AsyncMock(return_value=vacancy_factory(external_id=999)),
    ):
        response = await vacancies_client.post(
            "/api/v1/vacancies/",
            json=vacancy_payload_factory(external_id=999),
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Vacancy with external_id already exists"


async def test_create_vacancy_skips_conflict_check_when_external_id_is_none(
    vacancies_client, vacancy_payload_factory, vacancy_factory
):
    with patch(
        "app.api.v1.vacancies.get_vacancy_by_external_id",
        new=AsyncMock(return_value=vacancy_factory(external_id=777)),
    ) as by_external_id_mock, patch(
        "app.api.v1.vacancies.create_vacancy",
        new=AsyncMock(return_value=vacancy_factory(id=2, external_id=None)),
    ) as create_mock:
        response = await vacancies_client.post(
            "/api/v1/vacancies/",
            json=vacancy_payload_factory(external_id=None),
        )

    assert response.status_code == 201
    assert response.json()["id"] == 2
    by_external_id_mock.assert_not_awaited()
    create_mock.assert_awaited_once()


@pytest.mark.parametrize("external_id", [0, 2_147_483_648])
async def test_create_vacancy_with_out_of_range_external_id_returns_422(
    vacancies_client, vacancy_payload_factory, external_id
):
    response = await vacancies_client.post(
        "/api/v1/vacancies/",
        json=vacancy_payload_factory(external_id=external_id),
    )

    assert response.status_code == 422


async def test_update_vacancy_returns_404_when_target_missing(
    vacancies_client, vacancy_payload_factory
):
    with patch("app.api.v1.vacancies.get_vacancy", new=AsyncMock(return_value=None)):
        response = await vacancies_client.put(
            "/api/v1/vacancies/1",
            json=vacancy_payload_factory(),
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


async def test_update_vacancy_returns_409_on_external_id_conflict(
    vacancies_client, vacancy_payload_factory, vacancy_factory
):
    target = vacancy_factory(id=1, external_id=100)
    conflicting = vacancy_factory(id=2, external_id=200)

    with patch("app.api.v1.vacancies.get_vacancy", new=AsyncMock(return_value=target)), patch(
        "app.api.v1.vacancies.get_vacancy_by_external_id",
        new=AsyncMock(return_value=conflicting),
    ):
        response = await vacancies_client.put(
            "/api/v1/vacancies/1",
            json=vacancy_payload_factory(external_id=200),
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Vacancy with external_id already exists"


@pytest.mark.parametrize("external_id", [0, 2_147_483_648])
async def test_update_vacancy_with_out_of_range_external_id_returns_422(
    vacancies_client, vacancy_payload_factory, external_id
):
    response = await vacancies_client.put(
        "/api/v1/vacancies/1",
        json=vacancy_payload_factory(external_id=external_id),
    )

    assert response.status_code == 422


async def test_update_vacancy_allows_same_external_id_for_same_vacancy(
    vacancies_client, vacancy_payload_factory, vacancy_factory
):
    target = vacancy_factory(id=1, external_id=100, title="Before")
    updated = vacancy_factory(id=1, external_id=100, title="After")

    with patch("app.api.v1.vacancies.get_vacancy", new=AsyncMock(return_value=target)), patch(
        "app.api.v1.vacancies.get_vacancy_by_external_id",
        new=AsyncMock(return_value=target),
    ), patch(
        "app.api.v1.vacancies.update_vacancy",
        new=AsyncMock(return_value=updated),
    ) as update_mock:
        response = await vacancies_client.put(
            "/api/v1/vacancies/1",
            json=vacancy_payload_factory(external_id=100, title="After"),
        )

    assert response.status_code == 200
    assert response.json()["title"] == "After"
    update_mock.assert_awaited_once()


async def test_delete_vacancy_returns_404_when_target_missing(vacancies_client):
    with patch("app.api.v1.vacancies.get_vacancy", new=AsyncMock(return_value=None)):
        response = await vacancies_client.delete("/api/v1/vacancies/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


async def test_delete_vacancy_returns_204_on_success(vacancies_client, vacancy_factory):
    with patch(
        "app.api.v1.vacancies.get_vacancy",
        new=AsyncMock(return_value=vacancy_factory()),
    ), patch("app.api.v1.vacancies.delete_vacancy", new=AsyncMock()) as delete_mock:
        response = await vacancies_client.delete("/api/v1/vacancies/1")

    assert response.status_code == 204
    assert response.text == ""
    delete_mock.assert_awaited_once()
