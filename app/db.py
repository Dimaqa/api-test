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

async def insert_worker(conn, name, company):
    stmt = workers.insert().values(name=name, company=company)
    try:
        await conn.execute(stmt)
    except UniqueViolationError:
        try:
            stmt = update(workers).where(workers.c.name == name).values(company=company)
            await conn.execute(stmt)
        except:
            return 'There is no such company'
    return None
