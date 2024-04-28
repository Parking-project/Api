from extensions.databse_extension import Base
from ..interface import IWPUserMeta

class WPUserMeta(IWPUserMeta):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    @classmethod
    def get_user_id(cls, user_id: str):
        pass

    @classmethod
    def get_telegram_id(cls, telegram_id: int):
        pass
