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

    place_id = Column(String(36),
                      ForeignKey('wp_place.ID'), nullable=True, default=None)
    user_id = Column(String(36),
                     ForeignKey('wp_user.ID'), nullable=False)

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def add_place(self, place_id: int):
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
    def get_busy(cls, timestamp_begin: int, timestamp_end: int):
        pass

    @classmethod
    @abstractmethod
    def get_user_id(cls, user_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_state(cls, user_id: str, state: ReserveStatus):
        pass

    @classmethod
    @abstractmethod
    def get_hours(cls, hour: int):
        pass
