from aiohttp import web

from src.handlers import (
    handle_create,
    handle_read_all,
    handle_read_by_name,
    handle_read_by_age,
    handle_read_by_department,
    handle_update,
    handle_delete
)


def setup_routes(app: web.Application):
    """Настраивает эндпоинты"""
    app.router.add_post("/create", handle_create)
    app.router.add_get("/read/all", handle_read_all),
    app.router.add_get("/read/read_by_name", handle_read_by_name),
    app.router.add_get("/read/read_by_age", handle_read_by_age),
    app.router.add_get("/read/read_by_department", handle_read_by_department),
    app.router.add_put("/update", handle_update),
    app.router.add_delete("/delete", handle_delete)
