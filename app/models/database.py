from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import databases

DB_NAME = environ.get('DB_NAME', 'test_db')
DB_USER = environ.get('DB_USER', 'user')
DB_PASS = environ.get('DB_PASS', 'qwerty123')
DB_HOST = environ.get('DB_HOST', 'localhost')

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

database = databases.Database(url=SQLALCHEMY_DATABASE_URL)
SyncSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine))
