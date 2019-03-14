import asyncpgsa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)

metadata = MetaData()

companies = Table(
    'companies', metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
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
    await conn.execute(stmt)