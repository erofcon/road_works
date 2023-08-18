from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey

from .user import user
from .group import group

metadata = MetaData()

users_groups = Table('users_groups', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('user_id', Integer(), ForeignKey(user.c.id, ondelete='CASCADE')),
                     Column('group_id', Integer(), ForeignKey(group.c.id, ondelete='CASCADE'))
                     )
