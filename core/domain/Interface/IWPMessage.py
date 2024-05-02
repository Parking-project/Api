from extensions.databse_extension import Base
from sqlalchemy import Column, String, BigInteger, Text, Integer, Boolean, ForeignKey
from abc import abstractmethod

class IWPMessage(Base):
    __tablename__ = 'wp_message'

    ID = Column(String(36), primary_key=True)
    message_date = Column(BigInteger, nullable=False)
    message_text = Column(Text, nullable=True)
    message_iterator = Column(Integer, nullable=False, default=0)
    message_is_end = Column(Boolean, nullable=False, default=0)

    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=True)
    message_root_id = Column(String(36),
                               ForeignKey('wp_message.ID'), nullable=False)
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
    def get_message_id(cls, message_id: str, is_bot: bool = True):
        pass
