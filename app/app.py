from aiohttp import web
import json
from routes import setup_routes
from db import init_db

async def init_app():
    app = web.Application()
    await init_db(app)
    setup_routes(app)
    return app

app = init_app()
web.run_app(app)