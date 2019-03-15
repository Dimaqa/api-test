import asyncpgsa
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError, DataError
from sqlalchemy.sql import select, update
from db_tables import companies, workers, connection, products


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


async def insert_company(conn, name, phone=None):
    stmt = companies.insert().values(name=name, phone=phone)
    try:
        await conn.execute(stmt)
    except UniqueViolationError:
        return 'Company already exists'
    return None


async def insert_product(conn, name):
    stmt = products.insert().values(name=name)
    try:
        await conn.execute(stmt)
    except UniqueViolationError:
        return 'Products already exists'
    return None


async def insert_worker(conn, name, company):
    stmt = workers.insert().values(name=name, company=company)
    try:
        await conn.execute(stmt)
    except UniqueViolationError:
        try:
            stmt = update(workers).where(
                workers.c.name == name).values(company=company)
            await conn.execute(stmt)
        except ForeignKeyViolationError:
            return 'There is no such company'
    return None


async def edit_responsible(conn, product_id, worker_id):
    stmt = connection.insert().values(product_id=product_id, worker_id=worker_id)
    try:
        await conn.execute(stmt)
    except UniqueViolationError:
        stmt = update(connection).where(
            connection.c.product_id == product_id).values(worker_id=worker_id)
        await conn.execute(stmt)
    except ForeignKeyViolationError:
        return 'There is worker or product with such id'
    except DataError:
        return 'Not valid data format'
    # return current resposible list with (product : name) format
    stmt = select(
        [products.c.name, workers.c.name.label('uname')]).\
        select_from(products.
                    outerjoin(connection).
                    outerjoin(workers))

    data = await conn.fetch(stmt)
    records = dict(data)
    return records