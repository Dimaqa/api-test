from aiohttp import web
import json
from routes import setup_routes

app = web.Application()
setup_routes(app)
web.run_app(app)