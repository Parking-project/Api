from extensions.databse_extension import Base
from sqlalchemy import Column, String, BigInteger, ForeignKey
from datetime import datetime
from abc import abstractmethod

class IWPTokenBlocList(Base):
    __tablename__ = 'wp_token_bloclist'

    ID = Column(String(36), primary_key=True)
    token_jti = Column(String(255), nullable=False)
    token_create = Column(BigInteger, nullable=False, default=datetime.now().timestamp())

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get_jti(cls, jti):
        pass
