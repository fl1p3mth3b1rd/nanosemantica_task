import logging

from aiohttp import web
from asyncpg import connect
from webargs import aiohttpparser

from src.db import DB_URL
from src.schemas import (
    AllParamsRequest,
    GeneralResponse,
    ByNameRequest,
    ByAgeRequest,
    ByDepartmentRequest,
    UpdateRequest,
    AllParamsRequestSchema,
    GeneralResponseSchema,
    ByNameRequestSchema,
    ByAgeRequestSchema,
    ByDepartmentRequestSchema,
    UpdateRequestSchema
)
from src.helpers import ConvertRecordToList

async def handle_create(request: web.Request) -> web.Response:
    """Создание сотрудников"""
    create_request: AllParamsRequest = await aiohttpparser.parser.parse(
        argmap=AllParamsRequestSchema,
        req=request,
        location='json'
    )
    create_response = GeneralResponse(
        error=False,
        status_code=200,
        message='',
        payload=''
    )
    try:
        conn = await connect(DB_URL)
        row = await conn.fetchrow(
            """
            SELECT (name, age, department) 
            FROM users
            WHERE name = $1 AND age = $2 AND
              department = $3;
            """,
            create_request.name,
            create_request.age,
            create_request.department
        )
        if row is not None:
            raise web.HTTPConflict
        await conn.execute(
            "INSERT INTO users (name, age, department) VALUES ($1, $2, $3)",
            create_request.name,
            create_request.age,
            create_request.department
        )
        create_response.payload = f"""
        Сотрудник:
            Имя: {create_request.name},
            Возраст: {create_request.age},
            Отдел: {create_request.department}
        был создан."""
        create_response.message = "Сотрудник успешно создан"
        await conn.close()
    except web.HTTPConflict:
        create_response.error = True,
        create_response.status_code = 409
        create_response.message = "Такой сотрудник уже существует"
    except Exception:
        create_response.error = True,
        create_response.status_code = 500
        create_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(create_response))

async def handle_read_by_name(request: web.Request) -> web.Response:
    """Поиск сотрудников по имени"""
    read_by_name_request: ByNameRequest = await aiohttpparser.parser.parse (
        argmap=ByNameRequestSchema,
        req=request,
        location='query'
    )
    read_by_name_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        rows = await conn.fetch(
            """
            SELECT (name, age, department)
            FROM users
            WHERE name = $1
            """,
            read_by_name_request.name
        )
        if len(rows) == 0:
            raise web.HTTPNotFound
        rows = ConvertRecordToList(rows)
        read_by_name_response.message = "Запрос выполнен"
        read_by_name_response.payload = ",".join([
            f"name: {name}, age: {age}, dep: {dep}"
            for name, age, dep in rows
        ])
    except web.HTTPNotFound:
        read_by_name_response.error = True,
        read_by_name_response.status_code = 404
        read_by_name_response.message = \
            f"Сотрудников с именем {read_by_name_request.name} не существует"
    except Exception:
        read_by_name_response.error = True,
        read_by_name_response.status_code = 500
        read_by_name_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(read_by_name_response))

async def handle_read_by_age(request: web.Request) -> web.Response:
    """Поиск сотрудников по возрасту"""
    read_by_age_request: ByAgeRequest = await aiohttpparser.parser.parse (
        argmap=ByAgeRequestSchema,
        req=request,
        location='query'
    )
    read_by_age_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        rows = await conn.fetch(
            """
            SELECT (name, age, department)
            FROM users
            WHERE age = $1
            """,
            read_by_age_request.age
        )
        if len(rows) == 0:
            raise web.HTTPNotFound
        rows = ConvertRecordToList(rows)
        read_by_age_response.message = "Запрос выполнен"
        read_by_age_response.payload = ",".join([
            f"name: {name}, age: {age}, dep: {dep}"
            for name, age, dep in rows
        ])
    except web.HTTPNotFound:
        read_by_age_response.error = True,
        read_by_age_response.status_code = 404
        read_by_age_response.message = \
            f"Сотрудников с возрастом {read_by_age_request.age} не существует"
    except Exception:
        read_by_age_response.error = True,
        read_by_age_response.status_code = 500
        read_by_age_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(read_by_age_response))

async def handle_read_by_department(request: web.Request) -> web.Response:
    """Поиск сотрудников по отделу"""
    read_by_department_request: ByDepartmentRequest = await aiohttpparser.parser.parse (
        argmap=ByDepartmentRequestSchema,
        req=request,
        location='query'
    )
    read_by_department_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        rows = await conn.fetch(
            """
            SELECT (name, age, department)
            FROM users
            WHERE department = $1
            """,
            read_by_department_request.department
        )
        if len(rows) == 0:
            raise web.HTTPNotFound
        rows = ConvertRecordToList(rows)
        read_by_department_response.message = "Запрос выполнен"
        read_by_department_response.payload = ",".join([
            f"name: {name}, age: {age}, dep: {dep}"
            for name, age, dep in rows
        ])
    except web.HTTPNotFound:
        read_by_department_response.error = True,
        read_by_department_response.status_code = 404
        read_by_department_response.message = \
            f"Сотрудников в отделе {read_by_department_request.department} не найдено"
    except Exception:
        read_by_department_response.error = True,
        read_by_department_response.status_code = 500
        read_by_department_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(read_by_department_response))

async def handle_read_all(request: web.Request) -> web.Response:
    """Возвращает всех сотрудников"""
    read_all_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        rows = await conn.fetch(
            """
            SELECT *
            FROM users;
            """
        )
        if len(rows) == 0:
            raise web.HTTPNotFound
        rows = ConvertRecordToList(rows)
        read_all_response.payload = ", ".join([
            f"name: {name}, age: {age}, dep: {dep}"
            for name, age, dep in rows
        ])
    except web.HTTPNotFound:
        read_all_response.error = True,
        read_all_response.status_code = 404
        read_all_response.message = \
            f"Пока нет ни одного сотрудника"
    except Exception:
        read_all_response.error = True,
        read_all_response.status_code = 500
        read_all_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(read_all_response))

async def handle_update(request: web.Request) -> web.Response:
    """Обновление информации о сотруднике"""
    update_request: UpdateRequest = await aiohttpparser.parser.parse (
        argmap=UpdateRequestSchema,
        req=request,
        location='json'
    )
    update_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        affected_rows: str = await conn.execute(
            """
            UPDATE users 
            SET name = $1, age = $2,
              department = $3
            WHERE name = $4 AND age = $5 AND
              department = $6;
            """,
            update_request.new_name,
            update_request.new_age,
            update_request.new_department,
            update_request.name,
            update_request.age,
            update_request.department
        )
        if affected_rows == "UPDATE 0":
            raise web.HTTPNotFound
        update_response.message = \
            f"Запрос выполнен. Пользователей обновлено {affected_rows[-1]}"
        update_response.payload = ""
    except web.HTTPNotFound:
        update_response.error = True,
        update_response.status_code = 404
        update_response.message = f"Сотрудников с такими параметрами не обнаружено"
    except Exception:
        update_response.error = True,
        update_response.status_code = 500
        update_response.message = "Internal Server Error"
        logging.exception("Error")
    return web.json_response(GeneralResponseSchema().dump(update_response))

async def handle_delete(request: web.Request) -> web.Response:
    """Удаление сотрудника"""
    delete_request: AllParamsRequest = await aiohttpparser.parser.parse (
        argmap=AllParamsRequestSchema,
        req=request,
        location='json'
    )
    update_response = GeneralResponse(
        error=False,
        status_code=200,
        message=''
    )
    try:
        conn = await connect(DB_URL)
        affected_rows: str = await conn.execute(
            """
            DELETE FROM users
            WHERE name = $1 AND age = $2 AND
              department = $3;
            """,
            delete_request.name,
            delete_request.age,
            delete_request.department
        )
        if affected_rows == "DELETE 0":
            raise web.HTTPNotFound
        update_response.message = \
            f"Запрос выполнен. Пользователей удалено: {affected_rows[-1]}"
        update_response.payload = ""
    except web.HTTPNotFound:
        update_response.error = True,
        update_response.status_code = 404
        update_response.message = f"Сотрудников с такими параметрами не обнаружено"
    except Exception:
        update_response.error = True,
        update_response.status_code = 500
        update_response.message = "Internal Server Error"
        logging.exception("Error")

    return web.json_response(GeneralResponseSchema().dump(update_response))
