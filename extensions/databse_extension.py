from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import BooleanClauseList
from sqlalchemy.orm import Query

from config.database_config import DatabaseConfig

Base = declarative_base()
engine = create_engine(
    DatabaseConfig.CON_STRING,
    echo=True,
    connect_args={'user': DatabaseConfig.USER, 'password': DatabaseConfig.PASS})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


def sql_commit():
    session.commit()
    session.close()

# Добавляет запись
def sql_add(data):
    session.add(data)
    sql_commit()

# Удаляет запись
def sql_delete(data):
    session.delete(data)
    sql_commit()

# Получения записей
def sql_query(class_example, filter_condition: BooleanClauseList) -> Query:
    query_result = session.query(class_example).filter(filter_condition)
    session.close()
    return query_result
