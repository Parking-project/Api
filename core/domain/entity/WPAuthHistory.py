from core.domain.interface import IWPAuthHistory

from datetime import datetime
from sqlalchemy import desc
from uuid import uuid4

from extensions.databse_extension import sql_query, sql_add

class WPAuthHistory(IWPAuthHistory):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_id = kwargs.get("user_id")
        self.user_name = kwargs.get("user_name")
        self.auth_date = datetime.now().timestamp()

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index: int, page_size: int):
        select_classes = (WPAuthHistory,)
        filter_condition = (True)
        result = sql_query(
            select_classes,
            filter_condition=filter_condition
        ).\
            order_by(desc(WPAuthHistory.auth_date)).\
            offset(page_size*page_index).limit(page_size)
        if result.count() == 0:
            return []
        return result.all()
