from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float

from .detection import detection

metadata = MetaData()

detection_images = Table('detection_images', metadata,
                         Column('id', Integer(), primary_key=True),
                         Column('url', String()),
                         Column('latitude', Float()),
                         Column('longitude', Float()),
                         Column('detection_id', Integer(), ForeignKey(detection.c.id, ondelete='CASCADE')),
                         )
