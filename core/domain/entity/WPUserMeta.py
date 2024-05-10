from core.domain.interface import IWPUserMeta

from sqlalchemy import and_
from uuid import uuid4

from extensions.databse_extension import sql_query, sql_add, sql_delete

class WPUserMeta(IWPUserMeta):
    TELEGRAM_ID = "telegram_id"

    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_meta_key = kwargs.get('key')
        self.user_meta_value = str(kwargs.get('value'))
        self.user_id = kwargs.get('user_id')

    def save(self):
        sql_add(self)

    def delete(self):
        sql_delete(self)

    @classmethod
    def get_user_id(cls, user_id: str):
        select_classes = (WPUserMeta,)
        filter_condition = and_(WPUserMeta.user_id == user_id, 
                                WPUserMeta.user_meta_key == cls.TELEGRAM_ID)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_telegram_id(cls, telegram_id: int):
        select_classes = (WPUserMeta,)
        filter_condition = and_(WPUserMeta.user_meta_key == cls.TELEGRAM_ID,
                                WPUserMeta.user_meta_value == f"{telegram_id}")
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()
