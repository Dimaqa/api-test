import asyncpgsa

async def init_db(app):
    pool = await asyncpgsa.create_pool(
        host='localhost',
        port='5433',
        database='postgres',
        user='postgres',
        password='postgress',
    )
    app['db_pool'] = pool
    return pool