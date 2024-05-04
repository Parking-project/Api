from api.shared.global_exception import *
from core.domain.entity.WPUser import WPUser

class UserValidator:
    @classmethod
    def validate(cls, login: str, password: str, display_name: str):
        if len(login) < 6:
            raise DataError("Логин слишком короткий! (Минимум 6 символов)")
        if len(password) < 6:
            raise DataError("Пароль слишком короткий! (Минимум 6 символов)")
        if len(display_name) < 6:
            raise DataError("Пароль слишком короткий! (Минимум 6 символов)")
        
    @classmethod
    def validate_unique(cls, login: str):
        if WPUser.get_login(login).count() > 0:
            raise UniqueError("Логин")