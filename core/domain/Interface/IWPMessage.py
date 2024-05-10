from extensions.databse_extension import Base
from sqlalchemy import Column, String, BigInteger, Text, Integer, Boolean, ForeignKey
from abc import abstractmethod

class IWPMessage(Base):
    __tablename__ = 'wp_message'

    ID = Column(String(36), primary_key=True)
    message_date = Column(BigInteger, nullable=False)
    message_text = Column(Text, nullable=True)
    message_iterate = Column(Integer, nullable=False, default=0)
    message_is_end = Column(Boolean, nullable=False, default=0)

    message_bot_chat_telegram_id = Column(BigInteger, nullable=True)
    message_bot_telegram_id = Column(BigInteger, nullable=True)
    message_chat_telegram_id = Column(BigInteger, nullable=True)
    message_telegram_id = Column(BigInteger, nullable=True)

    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=True)
    message_root_id = Column(String(36),
                               ForeignKey('wp_message.ID'), nullable=False)
    message_answer_id = Column(String(36),
                               ForeignKey('wp_message.ID'), nullable=True)
    
    @abstractmethod
    def __init__(self, text: str, user_id: str, chat_id, message_tg_id, answer_message_id: int = None):
        pass

    @abstractmethod
    def set_bot_data(self, message_tg_id, chat_id):
        pass

    @abstractmethod
    def is_can_reply(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get(cls, page_index, page_size):
        pass

    @classmethod
    @abstractmethod
    def get_root_id(cls, root_id: str, page_index, page_size):
        pass

    @classmethod
    @abstractmethod
    def get_user_id(cls, user_id: str, page_index, page_size):
        pass
    
    @classmethod
    @abstractmethod
    def get_last_user_id(cls, user_id: str):
        pass
    
    @classmethod
    @abstractmethod
    def get_message_id(cls, message_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_message_bot_tg_id(cls, message_bot_id: int):
        pass
