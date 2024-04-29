from ..interface.IWPReserve import IWPReserve
from .WPPlace import WPPlace
from ..enum import ReserveStatus
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from uuid import uuid4

class WPReserve(IWPReserve):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.reserve_begin = kwargs.get('begin')
        self.reserve_end = kwargs.get('end')
        self.user_id = kwargs.get('user_id')

    def add_place(self, place_code: str):
        self.place_id = WPPlace.get_place_code(place_code).first().ID
        sql_commit()

    def approving(self):
        pass

    def paying(self):
        pass

    def delete(self):
        pass

    def save(self):
        pass

    @classmethod
    def get_reserve_id(cls, reserve_id: str):
        pass

    @classmethod
    def get_busy(cls, timestamp_begin: int, timestamp_end: int):
        pass

    @classmethod
    def get_user_id(cls, user_id: str):
        pass

    @classmethod
    def get_state(cls, user_id: str, state: ReserveStatus):
        pass

    @classmethod
    def get_hours(cls, hour: int):
        pass
