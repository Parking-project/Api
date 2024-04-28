from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from abc import ABC, abstractmethod

class IWPUserMeta(ABC):
    __tablename__ = 'wp_usermeta'

    ID = Column(String(36), primary_key=True)
    user_meta_key = Column(String(100), nullable=False)
    user_meta_value = Column(Text, nullable=False)

    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=False)
    user = relationship("WPUser", backref="metas")

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def get_user_id(cls, user_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_telegram_id(cls, telegram_id: int):
        pass
