from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from .user import user
from .task import task

metadata = MetaData()

answer = Table('answer', metadata,
               Column('id', Integer(), primary_key=True),
               Column('description', String(length=100)),
               Column('create_datetime', DateTime()),
               Column('task_id', Integer(), ForeignKey(task.c.id, ondelete='CASCADE')),
               Column('creator_id', Integer(), ForeignKey(user.c.id, ondelete='CASCADE')),
               )
