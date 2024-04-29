from extensions.databse_extension import Base
from sqlalchemy import Column, String, BigInteger, ForeignKey
from datetime import datetime
from abc import abstractmethod

class IWPAuthHistory(Base):
    __tablename__ = 'wp_auth_history'

    ID = Column(String(36), primary_key=True)
    auth_date = Column(BigInteger, nullable=False, default=datetime.now().timestamp())
    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=False)

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
