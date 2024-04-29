from ..interface.IWPUserMeta import IWPUserMeta
from extensions.databse_extension import sql_query, sql_add, sql_delete
from uuid import uuid4

TELEGRAM_ID = "telegram_id"

class WPUserMeta(IWPUserMeta):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_meta_key = kwargs.get('key')
        self.user_meta_value = kwargs.get('value')
        self.user_id = kwargs.get('user_id')

    def save(self):
        sql_add(self)

    def delete(self):
        sql_delete(self)

    @classmethod
    def get_user_id(cls, user_id: str):
        filter_condition = (WPUserMeta.user_id == user_id) & \
                           (WPUserMeta.user_meta_key == TELEGRAM_ID)
        return sql_query(WPUserMeta, filter_condition)

    @classmethod
    def get_telegram_id(cls, telegram_id: int):
        filter_condition = (WPUserMeta.user_meta_key == TELEGRAM_ID & \
                            WPUserMeta.user_meta_value == f"{telegram_id}")
        return sql_query(WPUserMeta, filter_condition)
