import requests


def get_login_token(base_url: str, username: str, password: str) -> str:
    body = {"email": username, "secret": password}
    url = base_url + "/api/authenticate"
    response = requests.post(url, json=body)
    response.raise_for_status()
    return response.json()["auth_token"]