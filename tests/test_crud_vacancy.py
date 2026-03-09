import asyncio
from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.crud.vacancy import (
    create_vacancy,
    delete_vacancy,
    get_vacancy,
    get_vacancy_by_external_id,
    list_vacancies,
    update_vacancy,
    upsert_external_vacancies,
)
from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyCreate, VacancyUpdate

pytestmark = pytest.mark.anyio


class _ScalarsResult:
    def __init__(self, values):
        self._values = values

    def all(self):
        return self._values


class _ExecuteResult:
    def __init__(self, one=None, many=None):
        self._one = one
        self._many = many if many is not None else []

    def scalar_one_or_none(self):
        return self._one

    def scalar_one(self):
        return self._one

    def scalars(self):
        return _ScalarsResult(self._many)


@pytest.mark.parametrize("vacancy_id", [1, 999])
async def test_get_vacancy_returns_value_from_session(
    mocked_session, vacancy_factory, vacancy_id
):
    expected = vacancy_factory(id=vacancy_id) if vacancy_id == 1 else None
    mocked_session.execute.return_value = _ExecuteResult(one=expected)

    result = await get_vacancy(mocked_session, vacancy_id=vacancy_id)

    assert result is expected
    mocked_session.execute.assert_awaited_once()


async def test_get_vacancy_by_external_id_returns_matching_row(
    mocked_session, vacancy_factory
):
    vacancy = vacancy_factory(id=3, external_id=555)
    mocked_session.execute.return_value = _ExecuteResult(one=vacancy)

    result = await get_vacancy_by_external_id(mocked_session, external_id=555)

    assert result is vacancy
    mocked_session.execute.assert_awaited_once()


@pytest.mark.parametrize(
    ("timetable_mode_name", "city_name", "expected_values"),
    [
        (None, None, set()),
        ("remote", None, {"%remote%"}),
        (None, "mos", {"%mos%"}),
        ("remote", "mos", {"%remote%", "%mos%"}),
    ],
)
async def test_list_vacancies_applies_filters_and_desc_order(
    mocked_session,
    vacancy_factory,
    timetable_mode_name,
    city_name,
    expected_values,
):
    vacancies = [vacancy_factory(), vacancy_factory(id=2, external_id=202)]
    mocked_session.execute.return_value = _ExecuteResult(many=vacancies)

    result = await list_vacancies(
        mocked_session,
        timetable_mode_name=timetable_mode_name,
        city_name=city_name,
    )

    assert result == vacancies
    statement = mocked_session.execute.call_args.args[0]
    sql = str(statement).lower()
    assert "order by" in sql
    assert "published_at" in sql
    compiled_params = set(statement.compile().params.values())
    assert expected_values.issubset(compiled_params)


async def test_create_vacancy_persists_and_refreshes_entity(mocked_session):
    data = VacancyCreate(
        external_id=777,
        title="SRE",
        timetable_mode_name="Hybrid",
        tag_name="Infra",
        city_name="SPb",
        published_at=datetime(2026, 2, 2, tzinfo=timezone.utc),
        is_remote_available=True,
        is_hot=False,
    )

    created = await create_vacancy(mocked_session, data)

    assert isinstance(created, Vacancy)
    assert created.external_id == 777
    mocked_session.add.assert_called_once_with(created)
    mocked_session.commit.assert_awaited_once()
    mocked_session.refresh.assert_awaited_once_with(created)


async def test_update_vacancy_overwrites_fields_and_refreshes(
    mocked_session, vacancy_factory
):
    vacancy = vacancy_factory(title="Old", city_name="Old City", external_id=101)
    payload = VacancyUpdate(
        external_id=222,
        title="New",
        timetable_mode_name="Office",
        tag_name="Platform",
        city_name="New City",
        published_at=datetime(2026, 3, 3, tzinfo=timezone.utc),
        is_remote_available=False,
        is_hot=True,
    )

    updated = await update_vacancy(mocked_session, vacancy, payload)

    assert updated is vacancy
    assert vacancy.title == "New"
    assert vacancy.external_id == 222
    assert vacancy.city_name == "New City"
    mocked_session.commit.assert_awaited_once()
    mocked_session.refresh.assert_awaited_once_with(vacancy)


async def test_delete_vacancy_deletes_row_and_commits(mocked_session, vacancy_factory):
    vacancy = vacancy_factory()

    await delete_vacancy(mocked_session, vacancy)

    mocked_session.delete.assert_awaited_once_with(vacancy)
    mocked_session.commit.assert_awaited_once()


async def test_upsert_external_vacancies_updates_existing_and_creates_new(
    mocked_session, vacancy_factory
):
    existing = vacancy_factory(id=10, external_id=101, title="Old title")
    mocked_session.execute.side_effect = [
        _ExecuteResult(many=[101]),
        _ExecuteResult(many=[existing]),
    ]
    payloads = [
        {
            "external_id": 101,
            "title": "New title",
            "timetable_mode_name": "Remote",
            "tag_name": "Backend",
            "city_name": "Moscow",
            "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": True,
        },
        {
            "external_id": 202,
            "title": "Brand new",
            "timetable_mode_name": "Office",
            "tag_name": "Frontend",
            "city_name": "Kazan",
            "published_at": datetime(2026, 2, 2, tzinfo=timezone.utc),
            "is_remote_available": False,
            "is_hot": False,
        },
        {
            "external_id": None,
            "title": "No external id",
            "timetable_mode_name": "Hybrid",
            "tag_name": "QA",
            "city_name": None,
            "published_at": datetime(2026, 2, 3, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": False,
        },
    ]

    created_count = await upsert_external_vacancies(mocked_session, payloads)

    assert created_count == 2
    assert existing.title == "New title"
    assert mocked_session.add.call_count == 2
    mocked_session.commit.assert_awaited_once()


async def test_upsert_external_vacancies_creates_rows_when_external_id_is_missing(
    mocked_session,
):
    payloads = [
        {
            "external_id": None,
            "title": "A",
            "timetable_mode_name": "Remote",
            "tag_name": "Backend",
            "city_name": None,
            "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": False,
        },
        {
            "external_id": None,
            "title": "B",
            "timetable_mode_name": "Office",
            "tag_name": "QA",
            "city_name": "SPb",
            "published_at": datetime(2026, 2, 2, tzinfo=timezone.utc),
            "is_remote_available": False,
            "is_hot": True,
        },
    ]

    created_count = await upsert_external_vacancies(mocked_session, payloads)

    assert created_count == 2
    assert mocked_session.execute.await_count == 0
    assert mocked_session.add.call_count == 2
    mocked_session.commit.assert_awaited_once()


class _RaceState:
    def __init__(self, participants):
        self.participants = participants
        self.persisted_external_ids = set()
        self.prefetch_calls = 0
        self.prefetch_ready = asyncio.Event()


class _RaceSession:
    def __init__(self, shared_state):
        self._state = shared_state
        self._pending = []

    async def execute(self, stmt):
        sql = str(stmt)
        if "SELECT vacancies.external_id" in sql:
            self._state.prefetch_calls += 1
            if self._state.prefetch_calls == self._state.participants:
                self._state.prefetch_ready.set()
            await self._state.prefetch_ready.wait()
            # Both sessions must read the same snapshot before any commit.
            return _ExecuteResult(many=[])
        raise AssertionError(f"Unexpected SQL in race test: {sql}")

    def add(self, vacancy):
        self._pending.append(vacancy.external_id)

    async def commit(self):
        for ext_id in self._pending:
            if ext_id in self._state.persisted_external_ids:
                self._pending.clear()
                raise IntegrityError("insert into vacancies", {"external_id": ext_id}, Exception("duplicate key"))
        self._state.persisted_external_ids.update(self._pending)
        self._pending.clear()


async def test_upsert_external_vacancies_race_condition_can_raise_integrity_error():
    payloads = [
        {
            "external_id": 404,
            "title": "Race case",
            "timetable_mode_name": "Remote",
            "tag_name": "Backend",
            "city_name": "Moscow",
            "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": False,
        }
    ]
    shared = _RaceState(participants=2)
    session_a = _RaceSession(shared)
    session_b = _RaceSession(shared)

    results = await asyncio.gather(
        upsert_external_vacancies(session_a, payloads),
        upsert_external_vacancies(session_b, payloads),
        return_exceptions=True,
    )

    successes = [result for result in results if result == 1]
    failures = [result for result in results if isinstance(result, IntegrityError)]
    assert len(successes) == 1
    assert len(failures) == 1


async def test_upsert_external_vacancies_accepts_reiterable_iterable_payloads(mocked_session):
    payloads = (
        {
            "external_id": 701,
            "title": "Tuple payload A",
            "timetable_mode_name": "Remote",
            "tag_name": "Backend",
            "city_name": "Moscow",
            "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
            "is_remote_available": True,
            "is_hot": False,
        },
        {
            "external_id": 702,
            "title": "Tuple payload B",
            "timetable_mode_name": "Office",
            "tag_name": "QA",
            "city_name": "SPb",
            "published_at": datetime(2026, 2, 2, tzinfo=timezone.utc),
            "is_remote_available": False,
            "is_hot": True,
        },
    )
    mocked_session.execute.return_value = _ExecuteResult(many=[])

    created_count = await upsert_external_vacancies(mocked_session, payloads)

    assert created_count == 2
    assert mocked_session.add.call_count == 2
    mocked_session.commit.assert_awaited_once()


async def test_upsert_external_vacancies_handles_iterator_payloads_without_data_loss(
    mocked_session,
):
    payloads = iter(
        [
            {
                "external_id": 801,
                "title": "Iterator payload A",
                "timetable_mode_name": "Remote",
                "tag_name": "Backend",
                "city_name": "Moscow",
                "published_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
                "is_remote_available": True,
                "is_hot": False,
            },
            {
                "external_id": 802,
                "title": "Iterator payload B",
                "timetable_mode_name": "Office",
                "tag_name": "QA",
                "city_name": "SPb",
                "published_at": datetime(2026, 2, 2, tzinfo=timezone.utc),
                "is_remote_available": False,
                "is_hot": True,
            },
        ]
    )
    mocked_session.execute.return_value = _ExecuteResult(many=[])

    created_count = await upsert_external_vacancies(mocked_session, payloads)

    assert created_count == 2
    assert mocked_session.add.call_count == 2
    mocked_session.commit.assert_awaited_once()
