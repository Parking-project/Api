from .base_requests import send_get_request

def get_aut_test(token):
    auth_get_request = "/auth/get"
    response = send_get_request(
        url=auth_get_request,
        data=None,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
    )
    return response.json()["auth"]