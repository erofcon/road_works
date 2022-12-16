from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from .users import users
from .tasks import tasks

metadata = MetaData()

answers = Table('answers', metadata,
                Column('id', Integer(), primary_key=True),
                Column('description', String()),
                Column('create_datetime', DateTime()),
                Column('task_id', Integer(), ForeignKey(tasks.c.id, ondelete='CASCADE')),
                Column('creator_id', Integer(), ForeignKey(users.c.id, ondelete='CASCADE')),
                )
