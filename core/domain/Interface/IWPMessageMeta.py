from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from abc import ABC, abstractmethod

class IWPMessageMeta(ABC):
    __tablename__ = 'wp_messagemeta'

    ID = Column(String(36), primary_key=True)
    message_meta_key = Column(String(100), nullable=False)
    message_meta_value = Column(Text, nullable=False)

    message_id = Column(String(36),
                     ForeignKey('wp_message.ID'), nullable=False)
    message = relationship("WPMessage", backref="metas")

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get_message_id(cls, message_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_message_bot_id(cls, message_bot_id: int):
        pass
