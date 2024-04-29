from werkzeug.exceptions import HTTPException


class CustomError(HTTPException):
    """ Custom Error Exception """
    code = 401

class UniqueError(CustomError):
    def __init__(self, name):
        self.description = f"{name} должен быть уникальным"

class PageError(CustomError):
    def __init__(self, reason):
        self.description = reason

class ConnectionError(CustomError):
    def __init__(self, sql_act):
        self.description = f"Соединение было прервано при выполнении метода - {sql_act}"

class SecurityError(CustomError):
    def __init__(self):
        self.description = f"Данное действие не доступно"

class DataError(CustomError):
    def __init__(self, reason):
        self.description = reason