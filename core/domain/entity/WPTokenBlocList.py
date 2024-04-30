from ..interface.IWPTokenBlocList import IWPTokenBlocList
from extensions.databse_extension import sql_query, sql_add
from uuid import uuid4

class WPTokenBlocList(IWPTokenBlocList):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.token_jti = kwargs.get("jti")

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        return sql_query(IWPTokenBlocList, (True)). \
                    offset(page_size * page_index).limit(page_size)

    @classmethod
    def get_jti(cls, jti):
        return sql_query(WPTokenBlocList, (WPTokenBlocList.token_jti == jti))
