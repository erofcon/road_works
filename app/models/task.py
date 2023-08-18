from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Float

from .user import user
from .group import group

metadata = MetaData()

task = Table('task', metadata,
             Column('id', Integer(), primary_key=True),
             Column('description', String(length=100)),
             Column('create_datetime', DateTime()),
             Column('lead_datetime', DateTime()),
             Column('latitude', Float()),
             Column('longitude', Float()),
             Column('is_done', Boolean(), default=False),
             Column('creator_id', Integer(), ForeignKey(user.c.id, ondelete='CASCADE')),
             Column('executor_id', Integer(), ForeignKey(user.c.id, ondelete='CASCADE')),
             Column('group_id', Integer(), ForeignKey(group.c.id, ondelete='CASCADE')),
             )
