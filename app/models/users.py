from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey

from .companies import companies

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('username', String(), unique=True),
              Column('password', String()),
              Column('name', String()),
              Column('surname', String()),
              Column('phone_number', Integer()),
              Column('email', String()),
              Column('is_super_user', Boolean(), default=False),
              Column('is_admin', Boolean(), default=False),
              Column('create_datetime', DateTime(), default=datetime.now()),
              Column('related_company', Integer(), ForeignKey(companies.c.id, ondelete='CASCADE'))
              )
