import asyncpgsa
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from sqlalchemy.sql import (select, update)

metadata = MetaData()

companies = Table(
    'companies', metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
    Column('phone', String(64), nullable=True)
)

workers = Table(
    'workers', metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
    Column('company', String(64), nullable=True),
    Column('phone', String(64), nullable=True)
)
products = Table(
    'products', metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
)
connection = Table(
    'connection', metadata,
    Column('worker_id', Integer, ForeignKey('workers.id')),
    Column('porduct_id', Integer, ForeignKey('product.id'))
)

async def init_db(app):
    pool = await asyncpgsa.create_pool(
        host='localhost',
        port='5432',
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
        try:
            stmt = update(connection).where(
                connection.c.product_id == product_id).values(worker_id=worker_id)
            await conn.execute(stmt)
        except ForeignKeyViolationError:
            return 'There is worker or product with such id'
    #return current resposible list with (product : name) format
    stmt = select(
        [products.c.name, workers.c.name.label('uname')]).\
        select_from(products. \
        outerjoin(connection). \
        outerjoin(workers))
    records = await conn.fetch(stmt)
    return records