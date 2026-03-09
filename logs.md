### Шаг Х

```bash
app-1  | 2026-03-08 20:25:38,408 | INFO | apscheduler.executors.default | Running job "_run_parse_job (trigger: interval[0:05:00], next run at: 2026-03-08 20:30:38 UTC)" (scheduled at 2026-03-08 20:25:38.403616+00:00)
app-1  | 2026-03-08 20:25:38,408 | INFO | app.services.parser | Старт парсинга вакансий
app-1  | 2026-03-08 20:25:38,443 | ERROR | app.services.parser | Ошибка парсинга вакансий: [Errno -5] No address associated with hostname
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
app-1  |     yield
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 394, in handle_async_request
app-1  |     resp = await self._pool.handle_async_request(req)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 256, in handle_async_request
app-1  |     raise exc from None
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 236, in handle_async_request
app-1  |     response = await connection.handle_async_request(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 101, in handle_async_request
app-1  |     raise exc
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 78, in handle_async_request
app-1  |     stream = await self._connect(request)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 124, in _connect
app-1  |     stream = await self._network_backend.connect_tcp(**kwargs)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/auto.py", line 31, in connect_tcp
app-1  |     return await self._backend.connect_tcp(
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/anyio.py", line 113, in connect_tcp
app-1  |     with map_exceptions(exc_map):
app-1  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
app-1  |     self.gen.throw(typ, value, traceback)
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
app-1  |     raise to_exc(exc) from exc
app-1  | httpcore.ConnectError: [Errno -5] No address associated with hostname
app-1  | 
app-1  | The above exception was the direct cause of the following exception:
app-1  | 
app-1  | Traceback (most recent call last):
app-1  |   File "/app/app/services/parser.py", line 34, in parse_and_store
app-1  |     payload = await fetch_page(client, page)
app-1  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/app/app/services/parser.py", line 17, in fetch_page
app-1  |     response = await client.get(
app-1  |                ^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1768, in get
app-1  |     return await self.request(
app-1  |            ^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1540, in request
app-1  |     return await self.send(request, auth=auth, follow_redirects=follow_redirects)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1629, in send
app-1  |     response = await self._send_handling_auth(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1657, in _send_handling_auth
app-1  |     response = await self._send_handling_redirects(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1694, in _send_handling_redirects
app-1  |     response = await self._send_single_request(request)
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1730, in _send_single_request
app-1  |     response = await transport.handle_async_request(request)
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 393, in handle_async_request
app-1  |     with map_httpcore_exceptions():
app-1  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
app-1  |     self.gen.throw(typ, value, traceback)
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
app-1  |     raise mapped_exc(message) from exc
app-1  | httpx.ConnectError: [Errno -5] No address associated with hostname
app-1  | 2026-03-08 20:25:38,445 | INFO | apscheduler.executors.default | Job "_run_parse_job (trigger: interval[0:05:00], next run at: 2026-03-08 20:30:38 UTC)" executed successfully
```


```bash
app-1  | INFO:     172.19.0.1:65354 - "DELETE /api/v1/vacancies/1231231222222222222222222222222222222222222222222222222222222222222 HTTP/1.1" 500 Internal Server Error
app-1  | ERROR:    Exception in ASGI application
app-1  | Traceback (most recent call last):
app-1  |   File "asyncpg/protocol/prepared_stmt.pyx", line 175, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
app-1  |   File "asyncpg/protocol/codecs/base.pyx", line 251, in asyncpg.protocol.protocol.Codec.encode
app-1  |   File "asyncpg/protocol/codecs/base.pyx", line 153, in asyncpg.protocol.protocol.Codec.encode_scalar
app-1  |   File "asyncpg/pgproto/codecs/int.pyx", line 60, in asyncpg.pgproto.pgproto.int4_encode
app-1  | OverflowError: value out of int32 range
app-1  | 
app-1  | The above exception was the direct cause of the following exception:
app-1  | 
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
app-1  |   File "asyncpg/protocol/protocol.pyx", line 184, in bind_execute
app-1  |   File "asyncpg/protocol/prepared_stmt.pyx", line 204, in asyncpg.protocol.protocol.PreparedStatementState._encode_bind_msg
app-1  | asyncpg.exceptions.DataError: invalid input for query argument $1: 1231231222222222222222222222222222222222... (value out of int32 range)
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
app-1  | sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 1231231222222222222222222222222222222222... (value out of int32 range)
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
app-1  |   File "/app/app/api/v1/vacancies.py", line 75, in delete_vacancy_endpoint
app-1  |     vacancy = await get_vacancy(session, vacancy_id)
app-1  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/app/app/crud/vacancy.py", line 11, in get_vacancy
app-1  |     result = await session.execute(select(Vacancy).where(Vacancy.id == vacancy_id))
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py", line 449, in execute
app-1  |     result = await greenlet_spawn(
app-1  |              ^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
app-1  |     result = context.throw(*sys.exc_info())
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
app-1  |     return self._execute_internal(
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2249, in _execute_internal
app-1  |     result: Result[Any] = compile_state_cls.orm_execute_statement(
app-1  |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
app-1  |     result = conn.execute(
app-1  |              ^^^^^^^^^^^^^
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
app-1  | sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: 1231231222222222222222222222222222222222... (value out of int32 range)
app-1  | [SQL: SELECT vacancies.id, vacancies.title, vacancies.timetable_mode_name, vacancies.tag_name, vacancies.city_name, vacancies.published_at, vacancies.is_remote_available, vacancies.is_hot, vacancies.created_at, vacancies.external_id 
app-1  | FROM vacancies 
app-1  | WHERE vacancies.id = $1::INTEGER]
app-1  | [parameters: (1231231222222222222222222222222222222222222222222222222222222222222,)]
app-1  | (Background on this error at: https://sqlalche.me/e/20/dbapi)

```


```bash
app-1  | 2026-03-08 20:57:39,143 | ERROR | app.services.parser | Ошибка парсинга вакансий: [Errno -2] Name or service not known
app-1  | Traceback (most recent call last):
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
app-1  |     yield
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 394, in handle_async_request
app-1  |     resp = await self._pool.handle_async_request(req)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 256, in handle_async_request
app-1  |     raise exc from None
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 236, in handle_async_request
app-1  |     response = await connection.handle_async_request(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 101, in handle_async_request
app-1  |     raise exc
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 78, in handle_async_request
app-1  |     stream = await self._connect(request)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 124, in _connect
app-1  |     stream = await self._network_backend.connect_tcp(**kwargs)
app-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/auto.py", line 31, in connect_tcp
app-1  |     return await self._backend.connect_tcp(
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/anyio.py", line 113, in connect_tcp
app-1  |     with map_exceptions(exc_map):
app-1  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
app-1  |     self.gen.throw(typ, value, traceback)
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
app-1  |     raise to_exc(exc) from exc
app-1  | httpcore.ConnectError: [Errno -2] Name or service not known
app-1  | 
app-1  | The above exception was the direct cause of the following exception:
app-1  | 
app-1  | Traceback (most recent call last):
app-1  |   File "/app/app/services/parser.py", line 34, in parse_and_store
app-1  |     payload = await fetch_page(client, page)
app-1  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/app/app/services/parser.py", line 17, in fetch_page
app-1  |     response = await client.get(
app-1  |                ^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1768, in get
app-1  |     return await self.request(
app-1  |            ^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1540, in request
app-1  |     return await self.send(request, auth=auth, follow_redirects=follow_redirects)
app-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1629, in send
app-1  |     response = await self._send_handling_auth(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1657, in _send_handling_auth
app-1  |     response = await self._send_handling_redirects(
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1694, in _send_handling_redirects
app-1  |     response = await self._send_single_request(request)
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1730, in _send_single_request
app-1  |     response = await transport.handle_async_request(request)
app-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 393, in handle_async_request
app-1  |     with map_httpcore_exceptions():
app-1  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
app-1  |     self.gen.throw(typ, value, traceback)
app-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
app-1  |     raise mapped_exc(message) from exc
app-1  | httpx.ConnectError: [Errno -2] Name or service not known
```