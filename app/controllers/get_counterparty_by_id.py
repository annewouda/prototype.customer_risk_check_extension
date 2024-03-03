import requests

from app.tools.get_access_token import get_login_token
from app.tools.make_logger import make_logger
from app.exceptions.exceptions import EnvironmentError

logger = make_logger(name="get_counterparty_by_id_logs")


def get_counter_party_by_id(environment: str, username: str, password: str, counterparty_id) -> requests.Response:
    if environment == "uat" or environment == "preprod":
        URL = f"https://{environment}.tradias.link"
    elif environment == "production":
        URL = "https://www.tradias.link"
    else: 
        raise EnvironmentError
    logger.info(f"Querying counterparty by ID for {environment}")
    path = f"/api/counter_parties/{counterparty_id}"
    secret = get_login_token(base_url=URL, username=username, password=password)
    headers = {"Authorization": f"Bearer {secret}"}
    response = requests.get(url=URL+path, headers=headers)
    logger.info(f"Received a {response.status_code}")
    return response



if __name__ == "__main__":
    from app.config.local_config import ANNE
    print(get_counter_party_by_id(environment="production",
                                  username=ANNE.username_production,
                                  password=ANNE.password_production,
                                  counterparty_id="7eee2a7f-7ecb-46ab-a768-c3ec0b502c3f").json())