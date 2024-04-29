from ..interface.IWPMessage import IWPMessage
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

class WPMessage(IWPMessage):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.message_text = kwargs.get('text')
        self.message_iterator = kwargs.get('iteration')
        self.user_id = kwargs.get('user_id')
        self.message_root_id = kwargs.get('root_id')
        self.message_answer_id = kwargs.get('answer_id')

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        return sql_query(WPMessage, (True)).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size)

    @classmethod
    def get_root_id(cls, root_id: str, page_index, page_size):
        filter_condition = (WPMessage.message_root_id == root_id | WPMessage.ID == root_id)
        return sql_query(WPMessage, filter_condition).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size)

    @classmethod
    def get_user_id(cls, user_id: str, page_index, page_size):
        filter_condition = (WPMessage.user_id == user_id | WPMessage.message_answer_id is None)
        return sql_query(WPMessage, filter_condition).order_by(WPMessage.message_date). \
                    offset(page_size * page_index).limit(page_size)
    
    @classmethod
    def get_message_id(cls, message_id: str, is_bot: bool = True):
        if is_bot:
            filter_condition = (WPMessage.ID == message_id) & \
                (WPMessage.user_id == None)
        else:
            filter_condition = (WPMessage.ID == message_id) & \
                (WPMessage.user_id != None)
        return sql_query(WPMessage, filter_condition)
