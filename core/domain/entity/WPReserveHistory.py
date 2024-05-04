from core.domain.interface import IWPReserveHistory

from extensions.databse_extension import sql_query

class WPReserveHistory(IWPReserveHistory):
    @classmethod
    def get(cls, page_index, page_size):
        result = sql_query(WPReserveHistory, (True)).\
            offset(page_size * page_index).\
            limit(page_size)
        if result.count() == 0:
            return []
        return result.all()
