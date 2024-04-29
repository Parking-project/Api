from ..interface.IWPUser import IWPUser
from extensions.databse_extension import sql_query, sql_add, sql_commit, sql_delete
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta
from uuid import uuid4
import hashlib
import os

class WPUser(IWPUser):
    def __init__(self, **kwargs):
        self.ID = uuid4()
        self.user_login = kwargs.get('login')
        self.set_password(kwargs.get('password'))
        self.user_display_name = kwargs.get('name')

    def set_password(self, password):
        salt = os.urandom(16)
        self.user_salt = salt.hex()
        self.user_pass = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    
    def update(self, display_name, role_id):
        self.user_display_name = display_name
        self.role_id = role_id
        sql_commit()

    def get_tokens(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        return {
            "access": create_access_token(
                identity = {
                    "user_id": self.ID,
                    "role_id": self.role_id
                },
                expires_delta=expire_delta
            ),
            "refresh": create_refresh_token(
                identity = {
                    "user_id": self.ID,
                    "role_id": self.role_id
                },
                expires_delta=expire_delta*6
            )
        }
    
    def save(self):
        sql_add(self)
    
    @classmethod
    def authenticate(cls, login: str, password: str):
        user: WPUser = WPUser.get_login(login).first()
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(user.user_salt), 100000).hex()
        if hashed_password != user.user_pass:
            raise Exception('Пользователя с таким логином или паролем не существует!')
        return user
    
    @classmethod
    def get_user_id(cls, user_id: str):
        filter_condition = (WPUser.ID == user_id)
        return sql_query(WPUser, filter_condition)
    
    @classmethod
    def get_login(cls, login: str):
        filter_condition = (WPUser.user_login == login)
        return sql_query(WPUser, filter_condition)
