from ..interface import IWPMessage
from .WPMessageMeta import WPMessageMeta
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

class WPMessage(IWPMessage):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.message_text = kwargs.get('text')
        self.user_id = kwargs.get('user_id')
        answer_tg_id = kwargs.get('answer_tg_id')
        if isinstance(answer_tg_id, int):
            self.message_answer_id = WPMessageMeta.get_message_id(message_tg_id=answer_tg_id)
        if self.message_answer_id is not None:
            answer_message: WPMessage = WPMessage.get_message_id(self.message_answer_id).first()
            self.message_root_id = answer_message.message_root_id
            self.message_iterator = answer_message.message_iterator + 1
        else:
            self.message_root_id = self.ID
        
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
        filter_condition = (WPMessage.user_id == user_id | WPMessage.message_answer_id is None)
        return sql_query(WPMessage, filter_condition).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size).order_by(WPMessage.message_date)
    
    @classmethod
    def get_message_id(cls, message_id: str):
        filter_condition = (WPMessage.ID == message_id)
        return sql_query(WPMessage, filter_condition)
