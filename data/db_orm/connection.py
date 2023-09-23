from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import DatabaseEnv


def get_reading_db_url():
    # url = 'sqlite:///teste.db'
    url = f"mysql+mysqlconnector://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    return url


def get_writing_db_url():
    # url = 'sqlite:///teste.db'
    url = f"mysql+mysqlconnector://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    return url


reading_engine = create_engine(get_reading_db_url(), echo=False)
writing_engine = create_engine(get_writing_db_url(), echo=False)

ReadingSession = sessionmaker(
    bind=reading_engine,
    class_=Session,
    autoflush=True,  # Takes updated object data from database
    autocommit=False,
    expire_on_commit=True,  # Remove object instance info
    info=None,
)

WritingSession = sessionmaker(
    bind=writing_engine,
    class_=Session,
    autoflush=True,  # Takes updated object data from database
    autocommit=False,
    expire_on_commit=True,  # Remove object instance info
    info=None,
)
