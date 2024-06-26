from extensions.databse_extension import Base
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from abc import abstractmethod

class IWPDocument(Base):
    __tablename__ = 'wp_document'

    ID = Column(String(36), primary_key=True)
    document_file_id = Column(String(100), nullable=True)
    document_file_unique_id = Column(String(100), nullable=True)
    document_file_size = Column(BigInteger, nullable=False)
    document_file_url = Column(Text, nullable=True)
    document_file_mime = Column(Text, nullable=True)

    message_id = Column(String(36),
                        ForeignKey('wp_message.ID'), nullable=False)
    message = relationship("WPMessage", backref="documents")

    @abstractmethod
    def __init__(self, message_id: str, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def get_message_id(cls, message_id: str):
        pass
