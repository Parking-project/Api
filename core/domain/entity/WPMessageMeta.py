from ..interface import IWPMessageMeta

class WPMessageMeta(IWPMessageMeta):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    @classmethod
    def get_message_id(cls, message_id: str):
        pass

    @classmethod
    def get_message_bot_id(cls, message_bot_id: int):
        pass
