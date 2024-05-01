from .token_test import login_test, logout_test, refresh_test
from .auth_test import get_aut_test

class AuthHistoryTest:
    ID: str
    auth_date: int
    user_id: str

    def __init__(self, **kwargs):
        self.ID = kwargs["ID"]
        self.auth_date = kwargs["auth_date"]
        self.user_id = kwargs["user_id"]

def main():
    access, refresh = login_test()
    logout_test(access)
    access = refresh_test(refresh)


    json_response = get_aut_test(access)
    auth_history = [AuthHistoryTest(**k) for k in json_response]
    print(auth_history)
