from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from .tasks import tasks

metadata = MetaData()

tasks_images = Table('tasks_images', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('url', String()),
                     Column('task_id', Integer(), ForeignKey(tasks.c.id, ondelete='CASCADE')),
                     )
