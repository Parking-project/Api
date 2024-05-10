from extensions.databse_extension import Base
from sqlalchemy import Column, String, Boolean
from abc import abstractmethod

class IWPPlace(Base):
    __tablename__ = 'wp_place'

    ID = Column(String(36), primary_key=True)
    place_is_valid = Column(Boolean, nullable=False, default=1)
    place_code = Column(String(4), nullable=False)
    
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
    def get_place_prefix(cls, place_prefix: str, page_index, page_size):
        pass

    @classmethod
    @abstractmethod
    def get_place_code(cls, place_code: str):
        pass

    @classmethod
    @abstractmethod
    def get_free(cls, reserve_list, page_index, page_size):
        pass
