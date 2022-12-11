from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from .users import users

metadata = MetaData()

detections = Table('detections', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('descriptions', String()),
                   Column('create_datetime', String()),
                   Column('creator_id', Integer(), ForeignKey(users.c.id, ondelete='CASCADE')),
                   )
