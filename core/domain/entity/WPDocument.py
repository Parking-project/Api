from ..interface.IWPDocument import IWPDocument
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from uuid import uuid4

class WPDocument(IWPDocument):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.document_file_id = kwargs.get('id')
        self.document_file_unique_id = kwargs.get('unique_id')
        self.document_file_size = kwargs.get('size')
        self.document_file_url = kwargs.get('url')
        self.document_file_mime = kwargs.get('mime')
        self.message_id = kwargs.get('message_id')

    def save(self):
        sql_add(self)

    @classmethod
    def get_document_id(cls, document_id: str):
        filter_condition = (WPDocument.ID == document_id)
        return sql_query(WPDocument, filter_condition)

    @classmethod
    def get_message_id(cls, message_id: str):
        filter_condition = (WPDocument.message_id == message_id)
        return sql_query(WPDocument, filter_condition)
