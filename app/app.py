from aiohttp import web
import json
from routes import setup_routes
from db import init_db
import aioredis
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage

async def setup_redis(app):

    pool = await aioredis.create_redis_pool((
        'redis://logs'
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool

async def init_app():
    app = web.Application()
    await init_db(app)
    redis_pool  = await setup_redis(app)
    setup_session(app, RedisStorage(redis_pool))
    setup_routes(app)
    return app

app = init_app()
web.run_app(app)
