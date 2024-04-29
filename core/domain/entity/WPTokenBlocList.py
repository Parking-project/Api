from ..interface.IWPTokenBlocList import IWPTokenBlocList
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from uuid import uuid4

class WPTokenBlocList(IWPTokenBlocList):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.token_jti = kwargs.get("jti")

    def save(self):
        sql_add(self)

    @classmethod
    def get_jti(cls, jti):
        return sql_query(WPTokenBlocList, (WPTokenBlocList.token_jti == jti))
