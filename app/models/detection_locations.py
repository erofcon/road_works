from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, Float

from .detection import detection

metadata = MetaData()

detection_locations = Table('detection_locations', metadata,
                            Column('id', Integer(), primary_key=True),
                            Column('latitude', Float()),
                            Column('longitude', Float()),
                            Column('detection_id', Integer(), ForeignKey(detection.c.id, ondelete='CASCADE')),
                            )
