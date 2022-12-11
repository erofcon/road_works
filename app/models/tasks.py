from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Float

from .users import users
from .groups import groups

metadata = MetaData()

tasks = Table('tasks', metadata,
              Column('id', Integer(), primary_key=True),
              Column('description', String()),
              Column('create_datetime', DateTime()),
              Column('lead_datetime', DateTime()),
              Column('latitude', Float()),
              Column('longitude', Float()),
              Column('is_done', Boolean(), default=False),
              Column('creator_id', Integer(), ForeignKey(users.c.id, ondelete='CASCADE')),
              Column('executor_id', Integer(), ForeignKey(users.c.id, ondelete='CASCADE')),
              Column('group_id', Integer(), ForeignKey(groups.c.id, ondelete='CASCADE')),
              )
