from core.domain.interface import IWPReserveHistory

from extensions.databse_extension import sql_query

class WPReserveHistory(IWPReserveHistory):
    @classmethod
    def get(cls, page_index, page_size):
        select_classes = (WPReserveHistory,)
        filter_condition = (True)
        result = sql_query(
            select_classes,
            filter_condition
        ).\
            order_by(WPReserveHistory.reserve_create).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()
