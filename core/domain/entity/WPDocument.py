from ..interface import IWPDocument

class WPDocument(IWPDocument):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    @classmethod
    def get_document_id(cls, document_id: str):
        pass

    @classmethod
    def get_message_id(cls, message_id: str):
        pass
