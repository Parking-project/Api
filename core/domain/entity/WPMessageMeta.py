from ..interface.IWPMessageMeta import IWPMessageMeta
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

MESSAGE_USER_TELEGRAM_ID = "message_user_telegram_id"
MESSAGE_BOT_TELEGRAM_ID = "message_bot_telegram_id"
MESSAGE_TELEGRAM_ID = "message_telegram_id"

class WPMessageMeta(IWPMessageMeta):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.message_meta_key = kwargs.get('message_meta_key')
        self.message_meta_value = kwargs.get('message_meta_value')
        self.message_id = kwargs.get('message_id')

    def save(self):
        sql_add(self)

    @classmethod
    def get_message_id(cls, message_id: str):
        filter_condition = (WPMessageMeta.message_id == message_id)
        return sql_query(WPMessageMeta, filter_condition)

    @classmethod
    def get_tg_bot_id(cls, tg_bot_id: int):
        filter_condition = (WPMessageMeta.message_meta_key == MESSAGE_BOT_TELEGRAM_ID & \
                            WPMessageMeta.message_meta_value == str(tg_bot_id))
        return sql_query(WPMessageMeta, filter_condition)

    @classmethod
    def get_tg_id(cls, tg_id: int):
        filter_condition = (WPMessageMeta.message_meta_key == MESSAGE_TELEGRAM_ID & \
                            WPMessageMeta.message_meta_value == str(tg_id))
        return sql_query(WPMessageMeta, filter_condition)

    @classmethod
    def get_tg_user_id(cls, tg_user_id: int):
        filter_condition = (WPMessageMeta.message_meta_key == MESSAGE_USER_TELEGRAM_ID & \
                            WPMessageMeta.message_meta_value == str(tg_user_id))
        return sql_query(WPMessageMeta, filter_condition)
