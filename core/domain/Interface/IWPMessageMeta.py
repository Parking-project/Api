from extensions.databse_extension import Base
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from abc import abstractmethod

class IWPMessageMeta(Base):
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
    def get(cls, message_id: str, key: str):
        pass