from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Query

from config.database_config import DatabaseConfig

from api.shared import ConnectionError

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
    except Exception as ex:
        raise ConnectionError(f"sql_commit - {ex}")

# Добавляет запись
def sql_add(data):
    try:
        session.add(data)
        sql_commit()
    except Exception as ex:
        raise ConnectionError(f"sql_add - {ex}")

# Удаляет запись
def sql_delete(data):
    try:
        session.delete(data)
        sql_commit()
    except:
        raise ConnectionError("sql_delete")

def sql_query1(cls1):
    try:
        return session.query(cls1)
    except Exception as ex:
        raise ConnectionError(f"sql_query: ({ex})")
    
# Получения записей
def sql_query(cls, filter_condition, inner_class=None, inner_condition=None):
    try:
        query = session.query(*cls)
        if inner_condition is not None and inner_class is not None:
            query = query.join(inner_class, inner_condition, isouter=True)
        query = query.filter(filter_condition)
        session.close()
        return query
    except Exception as ex:
        raise ConnectionError(f"sql_query: ({ex})")
