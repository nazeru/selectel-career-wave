from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.vacancy import Vacancy


@pytest.fixture
def vacancy_factory():
    def _factory(**overrides):
        payload = {
            "id": 1,
            "external_id": 101,
            "title": "Python Developer",
            "timetable_mode_name": "Remote",
            "tag_name": "Backend",
            "city_name": "Moscow",
            "published_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": False,
            "created_at": datetime(2026, 1, 1, 1, tzinfo=timezone.utc),
        }
        payload.update(overrides)
        return Vacancy(**payload)

    return _factory


@pytest.fixture
def vacancy_payload_factory():
    def _factory(**overrides):
        payload = {
            "external_id": 999,
            "title": "SRE",
            "timetable_mode_name": "Hybrid",
            "tag_name": "Infra",
            "city_name": "SPb",
            "published_at": "2026-03-01T10:00:00+00:00",
            "is_remote_available": True,
            "is_hot": False,
        }
        payload.update(overrides)
        return payload

    return _factory


@pytest.fixture
def mocked_session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.add = MagicMock()
    return session

