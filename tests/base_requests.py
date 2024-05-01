import requests  

base_url = "http://localhost:9098"
def send_get_request(url, data, headers):
    response = requests.get(
        url=base_url+url,
        params=data,
        json={},
        headers=headers
    )
    if response.status_code > 399:
        raise Exception(f"Status code is too big: {url} : {response.status_code}\n\n{response.content}")
    return response

def send_post_request(url, json, headers):
    response = requests.post(
        url=base_url+url,
        json=json,
        headers=headers
    )
    if response.status_code > 399:
        raise Exception(f"Status code is too big: {url} : {response.status_code}\n\n{response.content}")
    return response