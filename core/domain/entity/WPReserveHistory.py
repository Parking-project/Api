from extensions.databse_extension import sql_query
from ..interface import IWPReserveHistory

class WPReserveHistory(IWPReserveHistory):
    @classmethod
    def get(cls, page_index, page_size):
        return sql_query(WPReserveHistory, (True)). \
                    offset(page_size * page_index).limit(page_size)
