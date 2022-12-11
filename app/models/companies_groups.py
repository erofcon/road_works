from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey

from .companies import companies
from .groups import groups

metadata = MetaData()

companies_groups = Table('companies_groups', metadata,
                         Column('id', Integer(), primary_key=True),
                         Column('company_id', Integer(), ForeignKey(companies.c.id, ondelete='CASCADE')),
                         Column('group_id', Integer(), ForeignKey(groups.c.id, ondelete='CASCADE'))
                         )
