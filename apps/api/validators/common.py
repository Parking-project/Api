from ...shared.global_exception import PageError, DataError, SecurityError
from core.domain.entity.WPUser import WPUser
from core.domain.entity.WPRole import WPRole


class NoneValidator:
    @classmethod
    def validate(cls, data):
        if data is None:
            raise DataError(f"Данные не найдены {data}")
        return data

class JwtValidator:
    @classmethod
    def validate(cls, jwt, role_names: list[str]):
        user = WPUser.get_user_id(jwt["sub"]["user_id"]).first()
        role = WPRole.get_id(jwt["sub"]["role_id"]).first()
        if user is not None and role is not None:
            if role_names.count(role.role_name):
                return
        raise SecurityError()

class PageValidator:
    @classmethod
    def validate(cls, **kwargs):
        page_index = kwargs.get("page_index")
        page_size = kwargs.get("page_size")
        if not isinstance(page_index, int) or page_index is None:
            page_index = 0
        if not isinstance(page_size, int) or page_size is None:
            page_size = 10

        if page_size < 0:
            raise PageError("Размер страницы не может быть меньше 0!")
        if page_index < 0:
            raise PageError("Номер страницы не может быть меньше 0!")
        
        return page_index, page_size


class IsInt:
    def check(self, data):
        if isinstance(data, int):
            return
        raise DataError(f"{data} не является int")
    
class IsStr:
    def check(self, data):
        if isinstance(data, str):
            return
        raise DataError(f"{data} не является str")
    
class IsBool:
    def check(self, data):
        if isinstance(data, bool):
            return
        raise DataError(f"{data} не является bool")
    

class DataExistValidator:
    key_exist: dict

    def __init__(self, keys: dict):
        self.key_exist = keys

    def validate_exist(self, **kwargs):
        for key, value in self.key_exist.items():
            data = kwargs.get(key)
            NoneValidator.validate(data)
            value.check(data)