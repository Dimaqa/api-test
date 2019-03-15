from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)

metadata = MetaData()

connection = Table(
    'connection', metadata,

    Column('worker_id', Integer, ForeignKey('workers.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

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
    Column('phone', String(64), nullable=True),
)
products = Table(
    'products', metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False, unique=True),
)

