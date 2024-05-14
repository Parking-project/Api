from core.domain.interface import IWPDocument

from uuid import uuid4

from extensions.databse_extension import sql_query, sql_add

class WPDocument(IWPDocument):
    def __init__(self, message_id: str, **kwargs):
        self.ID = uuid4()
        self.document_file_id = kwargs.get('document_file_id')
        self.document_file_unique_id = kwargs.get('document_file_unique_id')
        self.document_file_size = kwargs.get('document_file_size')
        self.document_file_url = kwargs.get('document_file_url')
        self.document_file_mime = kwargs.get('document_file_mime')
        
        self.message_id = message_id

    def save(self):
        sql_add(self)

    @classmethod
    def get_message_id(cls, message_id: str):
        select_classes = (WPDocument,)
        filter_condition = (WPDocument.message_id == message_id)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_all(cls):
        select_classes = (WPDocument,)
        filter_condition = (True)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return []
        return result.all()
