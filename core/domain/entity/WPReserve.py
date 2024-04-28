from extensions.databse_extension import Base
from ..interface import IWPReserve
from ..enum import ReserveStatus

class WPReserve(IWPReserve):
    def __init__(self, **kwargs):
        pass

    def add_place(self, place_code: str):
        pass

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
