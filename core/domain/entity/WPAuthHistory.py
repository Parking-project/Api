from extensions.databse_extension import sql_query, sql_add
from ..interface import IWPAuthHistory
from datetime import datetime
from sqlalchemy import desc
from uuid import uuid4

class WPAuthHistory(IWPAuthHistory):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_id = kwargs.get("user_id")
        self.auth_date = datetime.now().timestamp()

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index: int, page_size: int):
        return sql_query(WPAuthHistory, (True)).\
            order_by(desc(WPAuthHistory.auth_date)).\
            offset(page_size*page_index).limit(page_size)
