from ..interface.IWPPlace import IWPPlace
from .WPReserve import WPReserve
from extensions.databse_extension import sql_query, sql_add, sql_commit
from uuid import uuid4

class WPPlace(IWPPlace):    
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.place_code = kwargs.get('code')

    def save(self):
        sql_add(self)

    def delete(self):
        self.place_is_valid = False
        sql_commit()

    @classmethod
    def get_place_prefix(cls, place_prefix: str, page_index, page_size):
        filter_condition = (WPPlace.place_code.contains(place_prefix))
        return sql_query(WPPlace, filter_condition). \
                    offset(page_size * page_index).limit(page_size)

    @classmethod
    def get_place_code(cls, place_code: str):
        filter_condition = (WPPlace.place_code == place_code)
        return sql_query(WPPlace, filter_condition)

    @classmethod
    def get_free(cls, hours: int, page_index, page_size):
        reserves = WPReserve.get_hours(hours)
        if reserves.count() > 0:
            filter_condition_place = (~WPPlace.ID.in_([x.place_id for x in reserves.all()]))
        else:
            filter_condition_place = (True)
        return sql_query(WPPlace, filter_condition_place). \
                    offset(page_size * page_index).limit(page_size)
