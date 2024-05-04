from extensions.databse_extension import sql_query, sql_add
from ..interface import IWPTokenBlocList
from datetime import datetime
from sqlalchemy import desc
from uuid import uuid4

class WPTokenBlocList(IWPTokenBlocList):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.token_jti = kwargs.get("jti")
        self.token_create = datetime.now().timestamp()

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        return sql_query(WPTokenBlocList, (True)).\
                    order_by(desc(WPTokenBlocList.token_create)). \
                    offset(page_size * page_index).limit(page_size)

    @classmethod
    def get_jti(cls, jti):
        return sql_query(WPTokenBlocList, (WPTokenBlocList.token_jti == jti))
