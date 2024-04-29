from ..interface.IWPRole import IWPRole
from extensions.databse_extension import sql_query

ADMIN_NAME = "ADMIN"
EMPLOYEE_NAME = "EMPLOYEE"
USER_NAME = "USER"

class WPRole(IWPRole):
    @classmethod
    def get(cls):
        return sql_query(WPRole, (True))

    @classmethod
    def get_id(cls, role_id: str):
        filter_condition = (WPRole.ID == role_id)
        return sql_query(WPRole, filter_condition)

    @classmethod
    def get_name(cls, role_name: str):
        filter_condition = (WPRole.role_name == role_name)
        return sql_query(WPRole, filter_condition)
