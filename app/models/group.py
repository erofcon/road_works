from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

metadata = MetaData()

group = Table('group', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(length=50), unique=True),
              Column('create_datetime', DateTime(), default=datetime.now()),
              )
