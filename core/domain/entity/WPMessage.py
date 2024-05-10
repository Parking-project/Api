from core.domain.interface import IWPMessage

from datetime import datetime
from sqlalchemy import desc
from sqlalchemy import or_
from uuid import uuid4

from extensions.databse_extension import sql_query, sql_commit, sql_add

class WPMessage(IWPMessage):   
    CHAT_ID = "chat_id"
    MESSAGE_BOT_ID = "message_bot_id"
    MESSAGE_ID = "message_id"  

    def __init__(self, text: str, user_id: str, chat_id, message_tg_id, answer_message_id: int = None):
        self.ID = uuid4()
        self.message_text = text
        self.user_id = user_id
        self.message_date = datetime.now().timestamp()
        
        self.message_telegram_id = message_tg_id
        self.message_chat_telegram_id = chat_id
        if answer_message_id is None:
            self.message_root_id = self.ID
            return
        
        self.message_answer_id = answer_message_id
        answer_message: WPMessage = WPMessage.get_message_id(answer_message_id)
        
        self.message_root_id = answer_message.message_root_id
        self.message_iterate = answer_message.message_iterate + 1
        
    def set_bot_data(self, message_tg_id, chat_id):
        self.message_bot_telegram_id = message_tg_id
        self.message_bot_chat_telegram_id = chat_id
        sql_commit()

    def is_can_reply(self):
        is_set_chat_id = self.message_chat_telegram_id is not None
        is_set_message_tg_id = self.message_telegram_id is not None
        return is_set_chat_id and is_set_message_tg_id

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        select_classes = (WPMessage,)
        filter_condition = (True)
        result = sql_query(
            select_classes,
            filter_condition
        ).\
            order_by(WPMessage.message_date).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_root_id(cls, root_id: str, page_index, page_size):
        select_classes = (WPMessage,)
        filter_condition = (WPMessage.message_root_id == root_id)
        result = sql_query(
            select_classes,
            filter_condition
        ).\
            order_by(WPMessage.message_date). \
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_user_id(cls, user_id: str, page_index, page_size):
        select_classes = (WPMessage,)
        filter_condition = or_(WPMessage.user_id == user_id, \
                            WPMessage.message_answer_id is None)
        result = sql_query(
            select_classes,
            filter_condition
        ).\
            order_by(desc(WPMessage.message_date)). \
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()
    
    @classmethod
    def get_last_user_id(cls, user_id: str):
        select_classes = (WPMessage,)
        filter_condition = (WPMessage.user_id == user_id)
        result = sql_query(
            select_classes,
            filter_condition
        ).\
            order_by(desc(WPMessage.message_date))
        if result.count() == 0:
            return None
        return result.first()
    
    @classmethod
    def get_message_id(cls, message_id: str):
        select_classes = (WPMessage,)
        filter_condition = (WPMessage.ID == message_id)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_message_bot_tg_id(cls, message_bot_id: int):
        select_classes = (WPMessage,)
        filter_condition = (WPMessage.message_bot_telegram_id == message_bot_id)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()
