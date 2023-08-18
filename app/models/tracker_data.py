from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, Float, ForeignKey

from .car import car

metadata = MetaData()

tracker_data = Table('tracker_data', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('latitude', Float()),
                     Column('longitude', Float()),
                     Column('create_datetime', DateTime(), default=datetime.now()),
                     Column('car_id', Integer(), ForeignKey(car.c.id, ondelete='CASCADE')),
                     )
