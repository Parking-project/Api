from api.shared import PageError, DataError, SecurityError
from core.domain.entity import WPRole

class NoneValidator:
    @classmethod
    def validate(cls, key, value):
        if value is None:
            raise DataError(f"Данные {key} не найдены")
        return value

class JwtValidator:
    @classmethod
    def validate(cls, jwt, role_names: list[str]):
        role: WPRole = WPRole.get_id(jwt["sub"]["role_id"])
        if role.role_name in role_names:
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
   
class IsExist:
    def check(self, data):
        return

class DataExistValidator:
    key_exist: dict

    def __init__(self, keys: dict):
        self.key_exist = keys

    def validate_exist(self, **kwargs):
        for key, value in self.key_exist.items():
            data = kwargs.get(key)
            NoneValidator.validate(key=key, value=data)
            value.check(data)