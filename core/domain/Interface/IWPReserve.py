from extensions.databse_extension import Base
from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from ..enum import ReserveStatus
from abc import abstractmethod

class IWPReserve(Base):
    __tablename__ = 'wp_reserve'

    ID = Column(String(36), primary_key=True)
    reserve_begin = Column(BigInteger, nullable=False)
    reserve_end = Column(BigInteger, nullable=False)
    reserve_state = Column(Integer, nullable=False, default=0)

    reserve_create = Column(BigInteger, nullable=False)

    reserve_message_id = Column(BigInteger, nullable=False)

    place_id = Column(String(36),
                      ForeignKey('wp_place.ID'), nullable=True, default=None)
    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=False)
    
    @abstractmethod
    def __init__(self, user_id: str, begin: int, end: int, **kwargs):
        pass

    @abstractmethod
    def set_message_id(self, message_id: int):
        pass

    @abstractmethod
    def set_place(self, place_id: str):
        pass

    @abstractmethod
    def approving(self):
        pass

    @abstractmethod
    def paying(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get_reserve_id(cls, reserve_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_actual_state(cls, user_id: str, states: list[int], page_index, page_size):
        pass

    @classmethod
    @abstractmethod
    def get_state(cls, user_id: str, states: list, page_index, page_size):
        pass

    @classmethod
    @abstractmethod
    def get_index(cls, user_id: str, states: list[ReserveStatus], index: int):
        pass

    @classmethod
    @abstractmethod
    def get_time_period(cls, begin: int, end: int):
        pass
