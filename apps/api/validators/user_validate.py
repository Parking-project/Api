from ...shared.global_exception import *
from core.domain.entity.WPUser import WPUser

class UserValidator:
    @classmethod
    def validate_register(cls, **kwargs):
        login = kwargs.get("login")
        password = kwargs.get("password")
        display_name = kwargs.get("display_name")
        if ~login:
            raise PageError("Логин не указан!")
        if len(login) < 6:
            raise PageError("Указанный логин слишком короткий!(минимум 6 символов)")
        if ~password:
            raise PageError("Пароль не указан!")
        if len(password) < 6:
            raise PageError("Указанный Пароль слишком короткий!(минимум 6 символов)")
        if ~display_name:
            raise PageError("Наименование не указан!")
        if len(display_name) < 6:
            raise PageError("Указанное наименование слишком короткое!(минимум 6 символов)")
    
    @classmethod
    def validate_unique(cls, **kwargs):
        if WPUser.get_login(**kwargs).count() != 0:
            raise UniqueError("Логин")  
