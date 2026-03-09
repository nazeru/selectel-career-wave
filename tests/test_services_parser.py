from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.core.config import settings
from app.services.parser import fetch_page, parse_and_store

pytestmark = pytest.mark.anyio


def make_external_response_dict(page, page_count, external_id, city_name=" Moscow "):
    return {
        "item_count": 1,
        "items": [
            {
                "id": external_id,
                "title": f"Title {external_id}",
                "timetable_mode": {"id": 1, "name": "Remote"},
                "tag": {"id": 1, "name": "Backend", "description": "desc"},
                "city": {"id": 1, "name": city_name} if city_name is not None else None,
                "published_at": datetime(2026, 3, page, tzinfo=timezone.utc).isoformat(),
                "is_remote_available": True,
                "is_hot": False,
            }
        ],
        "items_per_page": 1000,
        "page": page,
        "page_count": page_count,
    }


async def test_fetch_page_requests_expected_page_and_validates_payload():
    client = MagicMock()
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = make_external_response_dict(1, 1, 10)
    client.get = AsyncMock(return_value=response)

    payload = await fetch_page(client, page=3)

    client.get.assert_awaited_once_with(
        settings.api_url,
        params={"per_page": 1000, "page": 3},
    )
    response.raise_for_status.assert_called_once()
    assert payload.page == 1
    assert payload.page_count == 1
    assert payload.items[0].id == 10


async def test_parse_and_store_processes_all_pages_and_normalizes_city():
    session = object()
    fake_client = MagicMock()
    fake_client.aclose = AsyncMock()

    response_1 = MagicMock()
    response_1.raise_for_status = MagicMock()
    response_1.json.return_value = make_external_response_dict(1, 2, 100, " Moscow ")

    response_2 = MagicMock()
    response_2.raise_for_status = MagicMock()
    response_2.json.return_value = make_external_response_dict(2, 2, 200, None)

    fake_client.get = AsyncMock(side_effect=[response_1, response_2])

    with patch("app.services.parser.httpx.AsyncClient", return_value=fake_client), patch(
        "app.services.parser.upsert_external_vacancies",
        new=AsyncMock(side_effect=[2, 1]),
    ) as upsert_mock:
        created = await parse_and_store(session)

    assert created == 3
    assert fake_client.get.await_count == 2
    first_call = fake_client.get.await_args_list[0]
    second_call = fake_client.get.await_args_list[1]
    assert first_call.kwargs["params"]["page"] == 1
    assert second_call.kwargs["params"]["page"] == 2
    first_payload = upsert_mock.await_args_list[0].args[1][0]
    second_payload = upsert_mock.await_args_list[1].args[1][0]
    assert first_payload["city_name"] == "Moscow"
    assert second_payload["city_name"] is None
    fake_client.aclose.assert_awaited_once()


async def test_parse_and_store_handles_empty_page_items():
    session = object()
    fake_client = MagicMock()
    fake_client.aclose = AsyncMock()

    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "item_count": 0,
        "items": [],
        "items_per_page": 1000,
        "page": 1,
        "page_count": 1,
    }
    fake_client.get = AsyncMock(return_value=response)

    with patch("app.services.parser.httpx.AsyncClient", return_value=fake_client), patch(
        "app.services.parser.upsert_external_vacancies",
        new=AsyncMock(return_value=0),
    ) as upsert_mock:
        created = await parse_and_store(session)

    assert created == 0
    upsert_mock.assert_awaited_once_with(session, [])
    fake_client.aclose.assert_awaited_once()


@pytest.mark.parametrize("error_kind", ["request", "http_status"])
async def test_parse_and_store_returns_zero_on_http_errors(error_kind):
    session = object()
    fake_client = MagicMock()
    fake_client.aclose = AsyncMock()

    if error_kind == "request":
        fake_client.get = AsyncMock(side_effect=httpx.RequestError("network down"))
    else:
        request = httpx.Request("GET", settings.api_url)
        response = MagicMock()
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "upstream failed",
            request=request,
            response=httpx.Response(503, request=request),
        )
        response.json.return_value = {}
        fake_client.get = AsyncMock(return_value=response)

    with patch("app.services.parser.httpx.AsyncClient", return_value=fake_client), patch(
        "app.services.parser.upsert_external_vacancies",
        new=AsyncMock(),
    ) as upsert_mock:
        created = await parse_and_store(session)

    assert created == 0
    upsert_mock.assert_not_awaited()
    fake_client.aclose.assert_awaited_once()
