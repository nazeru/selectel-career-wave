### Шаг 1
Запустил 

```bash
docker compose up --build
```

Получил ошибку
```bash
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/bin/alembic", line 8, in <module>
app-1  |     sys.exit(main())
app-1  |              ^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/config.py", line 1047, in main
app-1  |     CommandLine(prog=prog).main(argv=argv)
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/config.py", line 1037, in main
app-1  |     self.run_cmd(cfg, options)
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/config.py", line 971, in run_cmd
app-1  |     fn(
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/command.py", line 483, in upgrade
app-1  |     script.run_env()
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/script/base.py", line 545, in run_env
app-1  |     util.load_python_file(self.dir, "env.py")
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/util/pyfiles.py", line 116, in load_python_file
app-1  |     module = load_module_py(module_id, path)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/alembic/util/pyfiles.py", line 136, in load_module_py
app-1  |     spec.loader.exec_module(module)  # type: ignore
app-1  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
app-1  |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
app-1  |   File "/app/alembic/env.py", line 8, in <module>
app-1  |     from app.core.config import settings
app-1  |   File "/app/app/core/config.py", line 20, in <module>
app-1  |     settings = Settings()
app-1  |                ^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/pydantic_settings/main.py", line 242, in __init__
app-1  |     super().__init__(**__pydantic_self__.__class__._settings_build_values(sources, init_kwargs))
app-1  |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 250, in __init__
app-1  |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
app-1  |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  | pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
app-1  | database_url
app-1  |   Extra inputs are not permitted [type=extra_forbidden, input_value='postgresql+asyncpg://pos...stgres@db:5432/postgres', input_type=str]
app-1  |     For further information visit https://errors.pydantic.dev/2.12/v/extra_forbidden
app-1 exited with code 1
```

Проверил файл config.py, нашел опечатку в алиасе 
```bash
validation_alias="DATABSE_URL",
```

Исправил на
```bash
validation_alias="DATABASE_URL",
```

Покрытие тестами:
- отдельный unit-тест для этого шага не добавлял, проверка через smoke (`docker compose up --build`) + успешный старт миграций

### Шаг 2
Запустил 

```bash
docker compose up --build
```

Проверил наличие таблицы, миграция применилась

Получил ошибку
```bash
app-1  | 2026-03-08 19:09:36,430 | INFO | httpx | HTTP Request: GET https://api.selectel.ru/proxy/public/employee/api/public/vacancies?per_page=1000&page=1 "HTTP/1.1 200 OK"
app-1  | 2026-03-08 19:09:36,431 | ERROR | app.main | Ошибка фонового парсинга: 'NoneType' object has no attribute 'name'
app-1  | Traceback (most recent call last):
app-1  |   File "/app/app/main.py", line 24, in _run_parse_job
app-1  |     await parse_and_store(session)
app-1  |   File "/app/app/services/parser.py", line 43, in parse_and_store
app-1  |     "city_name": item.city.name.strip(),
app-1  |                  ^^^^^^^^^^^^^^
app-1  | AttributeError: 'NoneType' object has no attribute 'name'
```

Сначала проверил что возвращает GET запрос, увидел что city может быть null
```json
{
      "city": null,
      "id": 1620,
      "is_hot": false,
      "is_remote_available": false,
      "published_at": "2026-03-05T13:06:17.976897+03:00",
      "tag": {
        "description": "Backend-разработка",
        "id": 1,
        "name": "backend"
      },
      "timetable_mode": {
        "id": 1,
        "name": "Гибкий"
      },
      "title": "Senior Golang-разработчик (KMS)"
    },
```

Открыл parser.py, вижу строку
```python
"city_name": item.city.name.strip(),
```

Открыл схему ExternalVacancyItem, проверил ее, поле city является Optional, гуд

Исправил на 
```python
"city_name": item.city.name.strip() if item.city else None,
```

Покрытие тестами:
- `tests/test_services_parser.py::test_parse_and_store_processes_all_pages_and_normalizes_city`

### Шаг 3
Запустил 

```bash
docker compose up --build
```

В логах вижу, что парсинг запустился, но повторяется каждые 5 секунд, вместо 5 минут, как заявлено в задании

Открыл scheduler.py, вижу, что указан атрибут seconds
```python
    scheduler.add_job(
        job,
        trigger="interval",
        seconds=settings.parse_schedule_minutes,
        coalesce=True,
        max_instances=1,
    )
```

Исправил на 
```python
        minutes=settings.parse_schedule_minutes,
```

Покрытие тестами:
- `tests/test_services_scheduler.py::test_create_scheduler_registers_single_interval_job`

### Шаг 4
Запустил 

```bash
docker compose up --build
```

Вижу что парсинг устанавливает интервал 5 минут

На всякий случай проверил соответствие объектов полученных от API и записанных в таблицу через ChatGPT, все гуд

Пробую удалить пару строк из таблицы и проверить парсинг новых вакансий, все корректно
Пробую изменить название вакансии в БД у случайной строки и посмотреть что будет после парсинга
Вижу, что название вакансии вернулось в актуальный вид после ручного обновление в БД, но в логе нет никакого упоминания что произошло обновление вакансии (считаю допущением, но я бы добавил дополнительное логирование о кол-ве обновленных вакансий)

Перехожу к проверке API

GET /api/v1/vacancies/ List Vacancies Endpoint
- данные корректны +
- фильтр по формату работы +
- фильтр по городу +
- фильтр одновременно по городу и формату работы +

POST /api/v1/vacancies/ Create Vacancy Endpoint
- создание работает +
- 200 при создании с существующим external_id вместо 409 (также создает JSONResponse вместо исключения HTTPException) -
- 422 при неверном payload +

Было:
```python
@router.post("/", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
async def create_vacancy_endpoint(
    payload: VacancyCreate, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    if payload.external_id is not None:
        existing = await get_vacancy_by_external_id(session, payload.external_id)
        if existing:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Vacancy with external_id already exists"},
            )
    return await create_vacancy(session, payload)
```

Стало
```python
@router.post("/", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
async def create_vacancy_endpoint(
    payload: VacancyCreate, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    if payload.external_id is not None:
        existing = await get_vacancy_by_external_id(session, payload.external_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vacancy with external_id already exists",
            )
    return await create_vacancy(session, payload)
```

Также удалил ненужный импорт JSONResponse

Покрытие тестами:
- `tests/test_api_vacancies.py::test_create_vacancy_returns_409_on_external_id_conflict`
- `tests/test_api_vacancies.py::test_create_vacancy_skips_conflict_check_when_external_id_is_none`

### Шаг 5

GET /api/v1/vacancies/{vacancy_id} Get Vacancy Endpoint
- получение по id работает + 
- 404 +

PUT /api/v1/vacancies/{vacancy_id} Update Vacancy Endpoint
- обновление работает +
- 500 при обновлении на существущий external_id -
- при отсутствие полей external_id или city_name в теле поле становится null +- (*Я предполагаю что это ожидаемое поведение так как у нас PUT, а не PATCH, в случае PATCH стоило бы обновлять только отправленные поля. Не исправлял, но можно было бы сделать exclude_unset=True*)

DELETE /api/v1/vacancies/{vacancy_id} Delete Vacancy Endpoint
- удаление работает +
- 404 + 

POST /api/v1/parse/ Parse Endpoint
- работает +
- проверил работу с учетом пагинации +

В ходе проверки выявил, что при обновлении поля external_id на уже существующий id выдает ответ 500
```bash
app-1  | INFO:     172.19.0.1:65398 - "PUT /api/v1/vacancies/63 HTTP/1.1" 500 Internal Server Error
app-1  | ERROR:    Exception in ASGI application
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 550, in _prepare_and_execute
app-1  |     self._rows = deque(await prepared_stmt.fetch(*parameters))
app-1  |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/prepared_stmt.py", line 177, in fetch
app-1  |     data = await self.__bind_execute(args, 0, timeout)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/prepared_stmt.py", line 268, in __bind_execute
app-1  |     data, status, _ = await self.__do_execute(
app-1  |                       ^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/prepared_stmt.py", line 257, in __do_execute
app-1  |     return await executor(protocol)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "asyncpg/protocol/protocol.pyx", line 205, in bind_execute
app-1  | asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint "uq_vacancies_external_id"
app-1  | DETAIL:  Key (external_id)=(1449) already exists.
app-1  | 
app-1  | The above exception was the direct cause of the following exception:
app-1  | 
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
app-1  |     self.dialect.do_execute(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
app-1  |     cursor.execute(statement, parameters)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 585, in execute
app-1  |     self._adapt_connection.await_(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
app-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
app-1  |     value = await result
app-1  |             ^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 563, in _prepare_and_execute
app-1  |     self._handle_exception(error)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 513, in _handle_exception
app-1  |     self._adapt_connection._handle_exception(error)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 797, in _handle_exception
app-1  |     raise translated_error from error
app-1  | sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.IntegrityError: <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "uq_vacancies_external_id"
app-1  | DETAIL:  Key (external_id)=(1449) already exists.
app-1  | 
app-1  | The above exception was the direct cause of the following exception:
app-1  | 
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
app-1  |     result = await app(  # type: ignore[func-returns-value]
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
app-1  |     return await self.app(scope, receive, send)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/applications.py", line 1160, in __call__
app-1  |     await super().__call__(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/applications.py", line 107, in __call__
app-1  |     await self.middleware_stack(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
app-1  |     raise exc
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
app-1  |     await self.app(scope, receive, _send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
app-1  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
app-1  |     raise exc
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
app-1  |     await app(scope, receive, sender)
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
app-1  |     await self.app(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 716, in __call__
app-1  |     await self.middleware_stack(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 736, in app
app-1  |     await route.handle(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/routing.py", line 290, in handle
app-1  |     await self.app(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 130, in app
app-1  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
app-1  |     raise exc
app-1  |   File "/usr/local/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
app-1  |     await app(scope, receive, sender)
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 116, in app
app-1  |     response = await f(request)
app-1  |                ^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 670, in app
app-1  |     raw_response = await run_endpoint_function(
app-1  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/fastapi/routing.py", line 324, in run_endpoint_function
app-1  |     return await dependant.call(**values)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/app/app/api/v1/vacancies.py", line 68, in update_vacancy_endpoint
app-1  |     return await update_vacancy(session, vacancy, payload)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/app/app/crud/vacancy.py", line 52, in update_vacancy
app-1  |     await session.commit()
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py", line 1000, in commit
app-1  |     await greenlet_spawn(self.sync_session.commit)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 203, in greenlet_spawn
app-1  |     result = context.switch(value)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2030, in commit
app-1  |     trans.commit(_to_root=True)
app-1  |   File "<string>", line 2, in commit
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
app-1  |     ret_value = fn(self, *arg, **kw)
app-1  |                 ^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1311, in commit
app-1  |     self._prepare_impl()
app-1  |   File "<string>", line 2, in _prepare_impl
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
app-1  |     ret_value = fn(self, *arg, **kw)
app-1  |                 ^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1286, in _prepare_impl
app-1  |     self.session.flush()
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 4331, in flush
app-1  |     self._flush(objects)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 4466, in _flush
app-1  |     with util.safe_reraise():
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 121, in __exit__
app-1  |     raise exc_value.with_traceback(exc_tb)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 4427, in _flush
app-1  |     flush_context.execute()
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py", line 466, in execute
app-1  |     rec.execute(self)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py", line 642, in execute
app-1  |     util.preloaded.orm_persistence.save_obj(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py", line 85, in save_obj
app-1  |     _emit_update_statements(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py", line 912, in _emit_update_statements
app-1  |     c = connection.execute(
app-1  |         ^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1419, in execute
app-1  |     return meth(
app-1  |            ^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 527, in _execute_on_connection
app-1  |     return connection._execute_clauseelement(
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1641, in _execute_clauseelement
app-1  |     ret = self._execute_context(
app-1  |           ^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
app-1  |     return self._exec_single_context(
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
app-1  |     self._handle_dbapi_exception(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2363, in _handle_dbapi_exception
app-1  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
app-1  |     self.dialect.do_execute(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
app-1  |     cursor.execute(statement, parameters)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 585, in execute
app-1  |     self._adapt_connection.await_(
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
app-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
app-1  |     value = await result
app-1  |             ^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 563, in _prepare_and_execute
app-1  |     self._handle_exception(error)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 513, in _handle_exception
app-1  |     self._adapt_connection._handle_exception(error)
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 797, in _handle_exception
app-1  |     raise translated_error from error
app-1  | sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "uq_vacancies_external_id"
app-1  | DETAIL:  Key (external_id)=(1449) already exists.
app-1  | [SQL: UPDATE vacancies SET external_id=$1::INTEGER WHERE vacancies.id = $2::INTEGER]
app-1  | [parameters: (1449, 63)]
app-1  | (Background on this error at: https://sqlalche.me/e/20/gkpj)
```

Открыл vacancies.py, вижу, что нет проверки на существующий external_id
```python
@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: int,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    vacancy = await get_vacancy(session, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return await update_vacancy(session, vacancy, payload)
```

Добавил проверку на существование external_id
```python
@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: int,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    vacancy = await get_vacancy(session, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if payload.external_id is not None:
        existing = await get_vacancy_by_external_id(session, payload.external_id)
        if existing and existing.id != vacancy.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vacancy with external_id already exists",
            )
    return await update_vacancy(session, vacancy, payload)
```

Покрытие тестами:
- `tests/test_api_vacancies.py::test_update_vacancy_returns_409_on_external_id_conflict`
- `tests/test_api_vacancies.py::test_update_vacancy_allows_same_external_id_for_same_vacancy`

### Шаг 6
Запустил 

```bash
docker compose up --build
```

Проверил обновление вакансии с заменой external_id на существующий, все ок

Увидел в crud.vacancy dict вместо set
```python
        existing_ids = {}
```

Изменил на
```python
        existing_ids = set()
```

(больше косметический фикс чем баг)

Покрытие тестами:
- отдельный тест не добавлял, так как изменение косметическое и не влияло на контракт API

### Шаг 7

Проверил более подробно парсер, заметил что AsyncClient не закрывает соединение

```python
async def parse_and_store(session: AsyncSession) -> int:
    logger.info("Старт парсинга вакансий")
    created_total = 0

    timeout = httpx.Timeout(10.0, read=20.0)
    try:
        client = httpx.AsyncClient(timeout=timeout)
        page = 1
        while True:
            payload = await fetch_page(client, page)
            parsed_payloads = []
            for item in payload.items:
                parsed_payloads.append(
                    {
                        "external_id": item.id,
                        "title": item.title,
                        "timetable_mode_name": item.timetable_mode.name,
                        "tag_name": item.tag.name,
                        "city_name": item.city.name.strip() if item.city else None,
                        "published_at": item.published_at,
                        "is_remote_available": item.is_remote_available,
                        "is_hot": item.is_hot,
                    }
                )

            created_count = await upsert_external_vacancies(session, parsed_payloads)
            created_total += created_count

            if page >= payload.page_count:
                break
            page += 1
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        logger.exception("Ошибка парсинга вакансий: %s", exc)
        return 0
```

Изменил на 
```python
async def parse_and_store(session: AsyncSession) -> int:
    logger.info("Старт парсинга вакансий")
    created_total = 0

    timeout = httpx.Timeout(10.0, read=20.0)
    client = httpx.AsyncClient(timeout=timeout)
    try:
        page = 1
        while True:
            payload = await fetch_page(client, page)
            parsed_payloads = []
            for item in payload.items:
                parsed_payloads.append(
                    {
                        "external_id": item.id,
                        "title": item.title,
                        "timetable_mode_name": item.timetable_mode.name,
                        "tag_name": item.tag.name,
                        "city_name": item.city.name.strip() if item.city else None,
                        "published_at": item.published_at,
                        "is_remote_available": item.is_remote_available,
                        "is_hot": item.is_hot,
                    }
                )

            created_count = await upsert_external_vacancies(session, parsed_payloads)
            created_total += created_count

            if page >= payload.page_count:
                break
            page += 1
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        logger.exception("Ошибка парсинга вакансий: %s", exc)
        return 0
    finally:
        await client.aclose()

    logger.info("Парсинг завершен, новых вакансий: %s", created_total)
    return created_total
```

Покрытие тестами:
- `tests/test_services_parser.py::test_parse_and_store_returns_zero_on_http_errors`
- `tests/test_services_parser.py::test_parse_and_store_handles_empty_page_items`
- в обоих кейсах дополнительно проверяется `fake_client.aclose.assert_awaited_once()`

### Шаг 8

Перешел к подробной проверке crud.vacancy, а именно метода upsert_external_vacancies

Нашел несколько проблем:

1) `payloads: Iterable[dict]` ломался на case с итератором  
Метод сначала итерировал `payloads` для сбора `external_id`, а потом второй раз проходил по `payloads` для upsert.  
Если передать `iter([...])`, второй проход уже пустой.

2) Дубли `external_id` внутри одного батча  
Если в одном `payloads` два элемента с одинаковым `external_id`, могла идти попытка создать две записи.

*Есть проблема N+1, но я думаю, что это больше перформанс улучшение, а не багфикс*

Было:
```python
async def upsert_external_vacancies(
    session: AsyncSession, payloads: Iterable[dict]
) -> int:
    external_ids = [payload["external_id"] for payload in payloads if payload["external_id"]]
    if external_ids:
        existing_result = await session.execute(
            select(Vacancy.external_id).where(Vacancy.external_id.in_(external_ids))
        )
        existing_ids = set(existing_result.scalars().all())
    else:
        existing_ids = set()

    created_count = 0
    for payload in payloads:
        ext_id = payload["external_id"]
        if ext_id and ext_id in existing_ids:
            result = await session.execute(
                select(Vacancy).where(Vacancy.external_id == ext_id)
            )
            vacancy = result.scalar_one()
            for field, value in payload.items():
                setattr(vacancy, field, value)
        else:
            session.add(Vacancy(**payload))
            created_count += 1

    await session.commit()
    return created_count
```

Изменил на:
```python
async def upsert_external_vacancies(
    session: AsyncSession, payloads: Iterable[dict]
) -> int:
    payload_items = list(payloads)
    external_ids = {
        payload["external_id"]
        for payload in payload_items
        if payload["external_id"] is not None
    }

    existing_vacancies_by_external_id: dict[int, Vacancy] = {}
    if external_ids:
        existing_result = await session.execute(
            select(Vacancy.external_id).where(Vacancy.external_id.in_(external_ids))
        )
        existing_ids = set(existing_result.scalars().all())
        if existing_ids:
            vacancies_result = await session.execute(
                select(Vacancy).where(Vacancy.external_id.in_(existing_ids))
            )
            existing_vacancies_by_external_id = {
                vacancy.external_id: vacancy
                for vacancy in vacancies_result.scalars().all()
                if vacancy.external_id is not None
            }
    else:
        existing_ids = set()

    created_count = 0
    for payload in payload_items:
        ext_id = payload["external_id"]
        vacancy = (
            existing_vacancies_by_external_id.get(ext_id)
            if ext_id is not None
            else None
        )
        if vacancy is not None:
            for field, value in payload.items():
                setattr(vacancy, field, value)
        else:
            created = Vacancy(**payload)
            session.add(created)
            if ext_id is not None:
                existing_vacancies_by_external_id[ext_id] = created
            created_count += 1

    await session.commit()
    return created_count
```

Итог:
- Поддержан `Iterable[dict]`, включая одноразовые итераторы
- Закрыт кейс дублей `external_id` внутри одного payload-батча

По гонке между двумя параллельными транзакциями:
- Конфликт ловится на unique constraint БД (`uq_vacancies_external_id`)
- Добавил тест, который фиксирует это поведение явно (один upsert успешен, второй получает `IntegrityError`)

Покрытие тестами:
- `tests/test_crud_vacancy.py::test_upsert_external_vacancies_handles_iterator_payloads_without_data_loss`
- `tests/test_crud_vacancy.py::test_upsert_external_vacancies_accepts_reiterable_iterable_payloads`
- `tests/test_crud_vacancy.py::test_upsert_external_vacancies_race_condition_can_raise_integrity_error`

### Дополнительно

1) В файле logs.md логи найденыых мною дополнительных ошибок, 2 сетевые ошибки и ошибки 500 при переполнении параметра {vacancy_id} в методах:
    - GET /api/v1/vacancies/{vacancy_id} Get Vacancy Endpoint
    - PUT /api/v1/vacancies/{vacancy_id} Update Vacancy Endpoint
    - DELETE /api/v1/vacancies/{vacancy_id} Delete Vacancy Endpoint

и при переполнении поля external_id в методах:
    - POST /api/v1/vacancies Create Vacancy Endpoint
    - PUT /api/v1/vacancies/{vacancy_id} Update Vacancy Endpoint

Было (vacancy_id без ограничения диапазона):
```python
@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    ...

@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: int,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    ...

@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    ...
```

Стало:
```python
VacancyId = Annotated[int, Path(ge=1, le=2_147_483_647)]

@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy_endpoint(
    vacancy_id: VacancyId, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    ...

@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: VacancyId,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    ...

@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy_endpoint(
    vacancy_id: VacancyId, session: AsyncSession = Depends(get_session)
) -> None:
    ...
```

Было (external_id без ограничения диапазона):
```python
class VacancyBase(BaseModel):
    ...
    external_id: Optional[int] = None
```

Стало:
```python
class VacancyBase(BaseModel):
    ...
    external_id: Optional[int] = Field(default=None, ge=1, le=2_147_483_647)
```

Итог:
- при выходе за диапазон в `vacancy_id` и `external_id` API возвращает `422`, а не `500`
- добавлены тесты на граничные значения в `tests/test_api_vacancies.py`

Покрытие тестами:
- `tests/test_api_vacancies.py::test_vacancy_id_out_of_range_returns_422`
- `tests/test_api_vacancies.py::test_create_vacancy_with_out_of_range_external_id_returns_422`
- `tests/test_api_vacancies.py::test_update_vacancy_with_out_of_range_external_id_returns_422`

2) Заменил константу API_URL на переменную окружения, удобно + был неиспользуемый импорт settings явно намекающий на это
3) Добавил явную типизацию в services.parser для parser_payloads, был тоже неиспользуемый List
4) убрал deprecated version из docker-compose

### Матрица исправлений

| № | Что было сломано | Где исправлено | Статус | Чем подтверждено |
|---|---|---|---|---|
| 1 | Неверный alias переменной БД (`DATABSE_URL`) | `app/core/config.py` (`Settings.database_url`) | Исправлено | Успешный запуск через `docker compose up --build`, миграции применяются |
| 2 | Падение парсера на `city=None` | `app/services/parser.py` (`parse_and_store`) | Исправлено | `tests/test_services_parser.py::test_parse_and_store_processes_all_pages_and_normalizes_city` |
| 3 | Неверный интервал фоновой задачи (секунды вместо минут) | `app/services/scheduler.py` (`create_scheduler`) | Исправлено | `tests/test_services_scheduler.py::test_create_scheduler_registers_single_interval_job` |
| 4 | `POST /vacancies` возвращал `200` вместо `409` при конфликте `external_id` | `app/api/v1/vacancies.py` (`create_vacancy_endpoint`) | Исправлено | `tests/test_api_vacancies.py::test_create_vacancy_returns_409_on_external_id_conflict` |
| 5 | `PUT /vacancies/{id}` мог падать `500` при конфликте `external_id` | `app/api/v1/vacancies.py` (`update_vacancy_endpoint`) | Исправлено | `tests/test_api_vacancies.py::test_update_vacancy_returns_409_on_external_id_conflict` |
| 6 | Не закрывался `httpx.AsyncClient` в парсере | `app/services/parser.py` (`parse_and_store`, `finally: await client.aclose()`) | Исправлено | `tests/test_services_parser.py::test_parse_and_store_returns_zero_on_http_errors`, `...handles_empty_page_items` |
| 7 | `upsert_external_vacancies` некорректно работал с `Iterable`/итератором | `app/crud/vacancy.py` (`upsert_external_vacancies`) | Исправлено | `tests/test_crud_vacancy.py::test_upsert_external_vacancies_handles_iterator_payloads_without_data_loss` |
| 8 | Дубли `external_id` в одном батче могли приводить к некорректному поведению | `app/crud/vacancy.py` (`upsert_external_vacancies`) | Исправлено | `tests/test_crud_vacancy.py::test_upsert_external_vacancies_accepts_reiterable_iterable_payloads` + race-тест |

Дополнительно (вне 8 базовых багов):
- Добавлена валидация диапазона `vacancy_id` в path (`1..2_147_483_647`) в `app/api/v1/vacancies.py`
- Добавлена валидация диапазона `external_id` (`1..2_147_483_647`) в `app/schemas/vacancy.py`
- Тесты:  
  `tests/test_api_vacancies.py::test_vacancy_id_out_of_range_returns_422`  
  `tests/test_api_vacancies.py::test_create_vacancy_with_out_of_range_external_id_returns_422`  
  `tests/test_api_vacancies.py::test_update_vacancy_with_out_of_range_external_id_returns_422`

### Summary

- Приложение запускается корректно, миграции применяются
- Фоновый парсинг работает стабильно и по расписанию в минутах
- CRUD API покрывает корректные статус-коды (`200/201/204/404/409/422`) по ключевым сценариям
- Критичные ошибки парсера и API обработаны без аварийных `500` в типичных пользовательских сценариях
- Тестовое покрытие актуализировано под внесенные фиксы

Финальная проверка:
```bash
./venv/bin/python -m pytest tests -q
# 43 passed
```
