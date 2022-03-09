from aiohttp import web
from aiohttp_swagger import setup_swagger

from src.settings import config
from src.routes import setup_routes
from src.db import create_dummy_db


def init_app(config) -> web.Application:
    """Инициализация приложения"""
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    return app

def start():
    """Запуск приложения"""
    # create_dummy_db()
    app = init_app(config)
    setup_swagger(app)
    web.run_app(app)

if "__main__" == __name__:
    start()
