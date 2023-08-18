from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean

metadata = MetaData()

company = Table('company', metadata,
                Column('id', Integer(), primary_key=True),
                Column('name', String(length=20), unique=True),
                Column('is_creator', Boolean(), default=False),
                Column('create_datetime', DateTime(), default=datetime.now()),
                )
