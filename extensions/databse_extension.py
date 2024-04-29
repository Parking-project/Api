from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import BooleanClauseList
from sqlalchemy.orm import Query

from config.database_config import DatabaseConfig

from apps.shared.global_exception import ConnectionError

Base = declarative_base()
engine = create_engine(
    url=DatabaseConfig.CON_STRING,
    echo=True,
    connect_args=
        {
            'user': DatabaseConfig.USER,
            'password': DatabaseConfig.PASS
        }
    )
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

def sql_commit():
    try:
        session.commit()
        session.close()
    except:
        raise ConnectionError("sql_commit")

# Добавляет запись
def sql_add(data):
    try:
        session.add(data)
        sql_commit()
    except:
        raise ConnectionError("sql_add")

# Удаляет запись
def sql_delete(data):
    try:
        session.delete(data)
        sql_commit()
    except:
        raise ConnectionError("sql_delete")

# Получения записей
def sql_query(class_example, filter_condition: BooleanClauseList) -> Query:
    try:
        query_result = session.query(class_example).filter(filter_condition)
        session.close()
        return query_result
    except:
        raise ConnectionError("sql_query")
