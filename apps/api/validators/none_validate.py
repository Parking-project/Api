from ...shared.global_exception import DataError

class NoneValidator:
    @classmethod
    def validate(cls, data):
        if data:
            return data
        raise DataError("Данные не найдены")