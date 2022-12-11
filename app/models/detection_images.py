from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float

from .detections import detections

metadata = MetaData()

detection_images = Table('detection_images', metadata,
                         Column('id', Integer(), primary_key=True),
                         Column('url', String()),
                         Column('latitude', Float()),
                         Column('longitude', Float()),
                         Column('detection_id', Integer(), ForeignKey(detections.c.id, ondelete='CASCADE')),
                         )
