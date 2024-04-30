from ..interface.IWPMessageMeta import IWPMessageMeta
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

MESSAGE_CHAT_TELEGRAM_ID = "message_chat_id"
MESSAGE_BOT_TELEGRAM_ID = "message_bot_id"
MESSAGE_TELEGRAM_ID = "message_id"

class WPMessageMeta(IWPMessageMeta):
    def __init__(self, message_id: str, key: str, value: str):
        self.ID = uuid4()
        self.message_meta_key = key
        self.message_meta_value = value
        self.message_id = message_id

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, message_id: str):
        filter_condition = (WPMessageMeta.message_id == message_id)
        return sql_query(WPMessageMeta, filter_condition)
    
    @classmethod
    def get_message_id(cls, message_tg_id: int):
        filter_condition = (WPMessageMeta.message_meta_key == MESSAGE_BOT_TELEGRAM_ID & \
                            WPMessageMeta.message_meta_value == str(message_tg_id))
        result = sql_query(WPMessageMeta, filter_condition).first()
        if result is None:
            return None
        return result.message_id
