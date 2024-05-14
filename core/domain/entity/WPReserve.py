from core.domain.interface import IWPReserve
from core.domain.enum import ReserveStatus

from sqlalchemy import or_, and_
from sqlalchemy import desc
from datetime import datetime
from uuid import uuid4

from core.domain.entity import WPPlace
from extensions.databse_extension import sql_query, sql_add, sql_commit

class WPReserve(IWPReserve):
    def __init__(self, user_id: str, begin: int, end: int, **kwargs):
        self.ID = uuid4()
        self.reserve_begin = begin
        self.reserve_end = end
        self.user_id = user_id
        self.reserve_state = ReserveStatus.SENDED.value
        self.reserve_create = datetime.now().timestamp()
        self.reserve_message_id = kwargs.get("message_id")

    def set_message_id(self, message_id: int):
        self.reserve_message_id = message_id

    def set_place(self, place_id: str):
        self.place_id = place_id
        sql_commit()

    def approving(self):
        self.reserve_state = ReserveStatus.APPROVE.value
        sql_commit()

    def paying(self):
        self.reserve_state = ReserveStatus.PAYED.value
        sql_commit()

    def delete(self):
        self.reserve_state = ReserveStatus.DELETED.value
        sql_commit()

    def save(self):
        sql_add(self)

    @classmethod
    def get_reserve_id(cls, reserve_id: str):
        select_classes = (WPReserve, )
        inner_class = None
        inner_condition = None
        filter_condition = (WPReserve.ID == reserve_id)
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        )
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_actual_state(cls, user_id: str, states: list[int], page_index, page_size):
        select_classes = (WPPlace, WPReserve)
        inner_class = WPPlace
        inner_condition = (WPReserve.place_id == WPPlace.ID)
        filter_condition = and_(
            WPReserve.reserve_state.in_(states),
            WPReserve.user_id == user_id,
            # WPReserve.reserve_end >= int(datetime.now().timestamp()
            # )
        )
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        ).\
            order_by(desc(WPReserve.reserve_create)).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_state(cls, user_id: str, states: list, page_index, page_size):
        select_classes = (WPPlace, WPReserve)
        inner_class = WPPlace
        inner_condition = (WPReserve.place_id == WPPlace.ID)
        filter_condition = and_(
            WPReserve.reserve_state.in_([1,2]),
            WPReserve.user_id == user_id
        )
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        ).\
            order_by(desc(WPReserve.reserve_create)).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get(cls, page_index, page_size):
        select_classes = (WPPlace, WPReserve)
        inner_class = WPPlace
        inner_condition = (WPReserve.place_id == WPPlace.ID)
        filter_condition = (True)
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        ).\
            order_by(desc(WPReserve.reserve_create)).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_index(cls, user_id: str, states: list[ReserveStatus], index: int):
        select_classes = (WPReserve,)
        inner_class = None
        inner_condition = None
        filter_condition = and_(
            WPReserve.user_id == user_id,
            WPReserve.reserve_state.in_(states),
            WPReserve.reserve_end >= int(datetime.now().timestamp())
        )
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        ).\
            order_by(desc(WPReserve.reserve_create)).\
            offset(index)
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_time_period(cls, begin: int, end: int):
        select_classes = (WPReserve,)
        inner_class = None
        inner_condition = None
        filter_condition = and_(
            WPReserve.place_id != None,
            or_(
                WPReserve.reserve_begin.between(begin, end),
                WPReserve.reserve_end.between(begin, end)
            ),

            WPReserve.reserve_state.in_([3,4])
        )
        result = sql_query(
            cls=select_classes,
            filter_condition=filter_condition,
            inner_class=inner_class,
            inner_condition=inner_condition
        )
        if result.count() == 0:
            return []
        return result.all()
