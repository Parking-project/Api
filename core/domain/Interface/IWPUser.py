from extensions.databse_extension import Base
from sqlalchemy import Column, String, ForeignKey, BigInteger
from abc import abstractmethod

class IWPUser(Base):
    __tablename__ = 'wp_user'

    ID = Column(String(36), primary_key=True)
    user_login = Column(String(255), nullable=False, unique=True)
    user_salt = Column(String(255), nullable=False)
    user_pass = Column(String(255), nullable=False)
    user_display_name = Column(String(255), nullable=False)
    user_registered = Column(BigInteger, nullable=False)

    role_id = Column(String(36),
                     ForeignKey('wp_role.ID'), nullable=False)
    
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def set_password(self, password: str):
        pass
    
    @abstractmethod
    def update(self, display_name, role_id):
        pass

    @abstractmethod
    def get_tokens(self, expire_time=24):
        pass
    
    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def is_user(self):
        pass

    @classmethod
    @abstractmethod
    def authenticate(cls, **kwargs):
        pass
    
    @classmethod
    @abstractmethod
    def get_user_id(cls, user_id: str):
        pass
    
    @classmethod
    @abstractmethod
    def get_login(cls, login: str):
        pass
    