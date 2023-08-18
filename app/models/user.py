from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric

from .company import company

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('username', String(length=20), unique=True),
             Column('password', String()),
             Column('name', String(length=20)),
             Column('surname', String(length=20)),
             Column('phone_number', Numeric()),
             Column('email', String(length=30)),
             Column('is_admin', Boolean(), default=False),
             Column('create_datetime', DateTime(), default=datetime.now()),
             Column('related_company', Integer(), ForeignKey(company.c.id, ondelete='CASCADE')),
             )
