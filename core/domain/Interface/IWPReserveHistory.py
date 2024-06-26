from extensions.databse_extension import Base
from sqlalchemy import Column, String, Integer, BigInteger
from abc import abstractmethod

class IWPReserveHistory(Base):
    __tablename__ = 'wp_reserve_history'

    ID = Column(String(36), primary_key=True)
    reserve_id = Column(String(36), nullable=False)
    reserve_state = Column(Integer, nullable=False, default=0)

    reserve_create = Column(BigInteger, nullable=False)

    @classmethod
    @abstractmethod
    def get(cls, page_index, page_size):
        pass
