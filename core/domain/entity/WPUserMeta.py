from core.domain.interface import IWPUserMeta

from extensions.databse_extension import sql_query, sql_add, sql_delete
from uuid import uuid4


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
        filter_condition = (WPUserMeta.user_id == user_id) and \
                           (WPUserMeta.user_meta_key == cls.TELEGRAM_ID)
        result = sql_query(WPUserMeta, filter_condition)
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_telegram_id(cls, telegram_id: int):
        filter_condition = (WPUserMeta.user_meta_key == cls.TELEGRAM_ID and \
                            WPUserMeta.user_meta_value == f"{telegram_id}")
        result = sql_query(WPUserMeta, filter_condition)
        if result.count() == 0:
            return None
        return result.first()
