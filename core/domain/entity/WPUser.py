from ..interface import IWPUser

class WPUser(IWPUser):
    def __init__(self, **kwargs):
        pass

    def set_password(self, password):
        pass

    def update(self, display_name, role_id):
        pass
    
    def get_tokens(self, expire_time=24):
        pass
    
    def save(self):
        pass
    
    @classmethod
    def authenticate(cls, login: str, password: str):
        pass
    
    @classmethod
    def get_user_id(cls, user_id: str):
        pass
    
    @classmethod
    def get_login(cls, login: str):
        pass
    
    @classmethod
    def get_telegram_id(cls, telegram_id: int):
        pass
