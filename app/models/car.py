from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

metadata = MetaData()

car = Table('car', metadata,
            Column('id', Integer(), primary_key=True),
            Column('imei', String(), unique=True),
            Column('car_number', String(length=10), default=False),
            Column('create_datetime', DateTime(), default=datetime.now()),
            )
