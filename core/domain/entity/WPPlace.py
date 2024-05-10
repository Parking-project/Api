from core.domain.interface import IWPPlace

from uuid import uuid4

from extensions.databse_extension import sql_query, sql_add, sql_commit

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
        select_classes = (WPPlace,)
        filter_condition = (WPPlace.place_code.contains(place_prefix))
        result = sql_query(
            select_classes, 
            filter_condition
        ).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_place_code(cls, place_code: str):
        select_classes = (WPPlace,)
        filter_condition = (WPPlace.place_code == place_code)
        result = sql_query(
            select_classes, 
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_free(cls, reserve_list, page_index, page_size):
        select_classes = (WPPlace,)
        if len(reserve_list) > 0:
            filter_condition = (~WPPlace.ID.in_([x.place_id for x in reserve_list]))
        else:
            filter_condition = (True)
        result = sql_query(
            select_classes, 
            filter_condition
        ).\
            offset(page_size * page_index).limit(page_size)
        if result.count() == 0:
            return []
        return result.all()
