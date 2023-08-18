from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from .answer import answer

metadata = MetaData()

answer_images = Table('answer_images', metadata,
                      Column('id', Integer(), primary_key=True),
                      Column('url', String()),
                      Column('answer_id', Integer(), ForeignKey(answer.c.id, ondelete='CASCADE')),
                      )
