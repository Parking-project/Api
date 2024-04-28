from extensions.databse_extension import Base
from sqlalchemy import Column, String
from abc import abstractmethod

class IWPRole(Base):
    __tablename__ = 'wp_role'

    ID = Column(String(36), primary_key=True)
    role_name = Column(String(255), nullable=False, unique=True)

    @classmethod
    @abstractmethod
    def get_id(cls, role_id: str):
        pass

    @classmethod
    @abstractmethod
    def get_name(cls, role_name: str):
        pass
