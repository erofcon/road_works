from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean

metadata = MetaData()

companies = Table('companies', metadata,
                  Column('id', Integer(), primary_key=True),
                  Column('name', String(), unique=True),
                  Column('is_creator', Boolean(), default=False),
                  Column('create_datetime', DateTime(), default=datetime.now()),
                  )
