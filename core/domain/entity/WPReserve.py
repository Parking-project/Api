from ..interface import IWPReserve
from ..enum import ReserveStatus
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from uuid import uuid4

class WPReserve(IWPReserve):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.reserve_begin = kwargs.get('begin')
        self.reserve_end = kwargs.get('end')
        self.user_id = kwargs.get('user_id')

    def add_place(self, place_id: int):
        self.place_id = place_id
        sql_commit()

    def approving(self):
        pass

    def paying(self):
        pass

    def delete(self):
        sql_delete(self)

    def save(self):
        sql_add(self)

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
