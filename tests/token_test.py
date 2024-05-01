from .base_requests import send_get_request, send_post_request

def login_test():
    login_request = "/token/login"
    response = send_post_request(
        url=login_request,
        json={
            "login": "user1",
            "password": "pass123"
        },
        headers={
            "Content-Type": "application/json",
        }
    )
    tokens = response.json()["tokens"]
    return tokens["access"], tokens["refresh"]

def refresh_test(refresh_token):
    login_request = "/token/refresh"
    response = send_get_request(
        url=login_request,
        data=None,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {refresh_token}",
        }
    )
    return response.json()["access"]

def logout_test(token):
    login_request = "/token/logout"
    response = send_get_request(
        url=login_request,
        data=None,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
    )
    return response.status_code