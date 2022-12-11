from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, Float, ForeignKey

from .car_data import car_data

metadata = MetaData()

tracker_data = Table('tracker_data', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('latitude', Float()),
                     Column('longitude', Float()),
                     Column('create_datetime', DateTime(), default=datetime.now()),
                     Column('imei_id', Integer(), ForeignKey(car_data.c.id, ondelete='CASCADE')),
                     )
