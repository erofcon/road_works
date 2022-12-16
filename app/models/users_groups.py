from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey

from .users import users
from .groups import groups

metadata = MetaData()

users_groups = Table('users_groups', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('user_id', Integer(), ForeignKey(users.c.id, ondelete='CASCADE')),
                     Column('group_id', Integer(), ForeignKey(groups.c.id, ondelete='CASCADE'))
                     )
