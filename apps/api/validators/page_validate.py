from ...shared.global_exception import PageError

class PageValidator:
    @classmethod
    def validate(cls, **kwargs):
        page_index = kwargs.get("page_index")
        page_size = kwargs.get("page_size")
        if ~page_index:
            kwargs[page_index] = 0
        if page_index < 0:
            raise PageError("Номер страницы не может быть меньше 0!")
        if page_size < 0:
            raise PageError("Размер страницы не может быть меньше 0!")