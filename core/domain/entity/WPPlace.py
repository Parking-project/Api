from extensions.databse_extension import Base
from ..interface import IWPPlace

class WPPlace(IWPPlace):
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    @classmethod
    def get_place_code(cls, place_code: str):
        pass

    @classmethod
    def get_free(cls, hours: int):
        pass
