from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from .answers import answers

metadata = MetaData()

answer_images = Table('answer_images', metadata,
                      Column('id', Integer(), primary_key=True),
                      Column('url', String()),
                      Column('answer_id', Integer(), ForeignKey(answers.c.id, ondelete='CASCADE')),
                      )
