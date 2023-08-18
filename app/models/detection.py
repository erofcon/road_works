from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from .user import user

metadata = MetaData()

detection = Table('detection', metadata,
                  Column('id', Integer(), primary_key=True),
                  Column('descriptions', String(length=20)),
                  Column('create_datetime', DateTime()),
                  Column('creator_id', Integer(), ForeignKey(user.c.id, ondelete='CASCADE')),
                  )
