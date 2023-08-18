from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from .task import task

metadata = MetaData()

task_images = Table('task_images', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('url', String()),
                    Column('task_id', Integer(), ForeignKey(task.c.id, ondelete='CASCADE')),
                    )
