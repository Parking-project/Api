from ..interface import IWPPlace
from extensions.databse_extension import sql_query

class WPPlace(IWPPlace):    
    def __init__(self, **kwargs):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    @classmethod
    def get_place_code(cls, place_code: str):
        return sql_query(WPPlace, (WPPlace.place_code == place_code))

    @classmethod
    def get_free(cls, hours: int):
        pass
