from core.domain.interface import IWPRole

from extensions.databse_extension import sql_query


class WPRole(IWPRole):
    ADMIN_NAME = "ADMIN"
    EMPLOYEE_NAME = "EMPLOYEE"
    USER_NAME = "USER"
    
    @classmethod
    def get(cls):
        result = sql_query(WPRole, (True))
        return result.all()

    @classmethod
    def get_id(cls, role_id: str):
        filter_condition = (WPRole.ID == role_id)
        result = sql_query(WPRole, filter_condition)
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_name(cls, role_name: str):
        filter_condition = (WPRole.role_name == role_name)
        result = sql_query(WPRole, filter_condition)
        if result.count() == 0:
            return None
        return result.first()
