from ..interface.IWPDocument import IWPDocument
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

class WPDocument(IWPDocument):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.document_file_id = kwargs.get('document_file_id')
        self.document_file_unique_id = kwargs.get('document_file_unique_id')
        self.document_file_size = kwargs.get('document_file_size')
        self.document_file_url = kwargs.get('document_file_url')
        self.document_file_mime = kwargs.get('document_file_mime')
        self.message_id = kwargs.get('message_id')

    def save(self):
        sql_add(self)

    @classmethod
    def get_message_id(cls, message_id: str):
        filter_condition = (WPDocument.message_id == message_id)
        return sql_query(WPDocument, filter_condition)
