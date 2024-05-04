from sqlalchemy import desc
from ..interface import IWPMessage
from .WPMessageMeta import WPMessageMeta
from extensions.databse_extension import sql_query, sql_add
from datetime import datetime
from uuid import uuid4

class WPMessage(IWPMessage):        
    def __init__(self, text: str, user_id: str, answer_message_id: int = None):
        self.ID = uuid4()
        self.message_text = text
        self.user_id = user_id
        self.message_date = datetime.now().timestamp()
        if answer_message_id is None:
            self.message_root_id = self.ID
            return
        
        self.message_answer_id = answer_message_id
        answer_message: WPMessage = WPMessage.get_message_id(answer_message_id).first()
        
        self.message_root_id = answer_message.message_root_id
        self.message_iterate = answer_message.message_iterate + 1
        
    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        return sql_query(WPMessage, (True)).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size).order_by(WPMessage.message_date)

    @classmethod
    def get_root_id(cls, root_id: str, page_index, page_size):
        filter_condition = (WPMessage.message_root_id == root_id | WPMessage.ID == root_id)
        return sql_query(WPMessage, filter_condition).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size).order_by(WPMessage.message_date)

    @classmethod
    def get_user_id(cls, user_id: str, page_index, page_size):
        filter_condition = (WPMessage.user_id == user_id or WPMessage.message_answer_id is None)
        return sql_query(WPMessage, filter_condition).order_by(WPMessage.message_date).\
                    order_by(desc(WPMessage.message_date)). \
                    offset(page_size * page_index).limit(page_size)
    
    @classmethod
    def get_message_id(cls, message_id: str):
        filter_condition = (WPMessage.ID == message_id)
        return sql_query(WPMessage, filter_condition)


    @classmethod
    def get_first_user_id(cls, user_id: str):
        filter_condition = (WPMessage.user_id == user_id)
        return sql_query(WPMessage, filter_condition). \
                    order_by(desc(WPMessage.message_date))