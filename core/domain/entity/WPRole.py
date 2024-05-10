from core.domain.interface import IWPRole

from extensions.databse_extension import sql_query

class WPRole(IWPRole):
    ADMIN_NAME = "ADMIN"
    EMPLOYEE_NAME = "EMPLOYEE"
    USER_NAME = "USER"
    
    @classmethod
    def get(cls):
        select_classes = (WPRole,)
        filter_condition = (True)
        result = sql_query(
            select_classes,
            filter_condition
        )
        return result.all()

    @classmethod
    def get_id(cls, role_id: str):
        select_classes = (WPRole,)
        filter_condition = (WPRole.ID == role_id)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()

    @classmethod
    def get_name(cls, role_name: str):
        select_classes = (WPRole,)
        filter_condition = (WPRole.role_name == role_name)
        result = sql_query(
            select_classes,
            filter_condition
        )
        if result.count() == 0:
            return None
        return result.first()
