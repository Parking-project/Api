from extensions.databse_extension import Base
from ..Interface import IWPMessage

class WPMessage(Base, IWPMessage):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    @classmethod
    def get_root_id(cls, root_id: int):
        pass

    @classmethod
    def get_user_id(cls, user_id: int):
        pass
    
    @classmethod
    def get_message_bot_id(cls, message_bot_id: int, is_bot: bool = True):
        pass
