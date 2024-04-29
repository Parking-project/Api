from ..interface.IWPAuthHistory import IWPAuthHistory
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from uuid import uuid4

class WPAuthHistory(IWPAuthHistory):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_id = kwargs.get("user_id")

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        sql_query(WPAuthHistory, (True)).order_by(WPAuthHistory.auth_date).\
            offset(page_index*page_size).limit(page_size)
