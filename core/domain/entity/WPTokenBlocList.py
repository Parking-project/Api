from core.domain.interface import IWPTokenBlocList

from datetime import datetime
from sqlalchemy import desc
from uuid import uuid4

from extensions.databse_extension import sql_query, sql_add

class WPTokenBlocList(IWPTokenBlocList):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.token_jti = kwargs.get("jti")
        self.token_create = datetime.now().timestamp()

    def save(self):
        sql_add(self)

    @classmethod
    def get(cls, page_index, page_size):
        select_classes = (WPTokenBlocList,)
        filter_condition = (True)
        result = sql_query(
            select_classes, 
            filter_condition
        ).\
            order_by(desc(WPTokenBlocList.token_create)). \
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()

    @classmethod
    def get_jti(cls, jti):
        select_classes = (WPTokenBlocList,)
        filter_condition = (WPTokenBlocList.token_jti == jti)
        return sql_query(
            select_classes,
            filter_condition
        )
