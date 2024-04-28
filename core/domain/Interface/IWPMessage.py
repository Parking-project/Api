from sqlalchemy import Column, String, BigInteger, Text, Integer, ForeignKey
from datetime import datetime
from abc import ABC, abstractmethod

class IWPMessage(ABC):
    __tablename__ = 'wp_message'

    ID = Column(String(36), primary_key=True)
    message_date = Column(BigInteger, nullable=False, default=datetime.now().timestamp())
    message_text = Column(Text, nullable=True)
    message_iterator = Column(Integer, nullable=False, default=0)

    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=True)
    message_root_id = Column(String(36),
                               ForeignKey('wp_message.ID'), nullable=True)
    message_answer_id = Column(String(36),
                               ForeignKey('wp_message.ID'), nullable=True)
    
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get_root_id(cls, root_id: int):
        pass

    @classmethod
    @abstractmethod
    def get_user_id(cls, user_id: int):
        pass
    
    @classmethod
    @abstractmethod
    def get_message_bot_id(cls, message_bot_id: int, is_bot: bool = True):
        pass
