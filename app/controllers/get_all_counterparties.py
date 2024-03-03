import requests

from app.tools.get_access_token import get_login_token
from app.tools.make_logger import make_logger
from app.exceptions.exceptions import EnvironmentError


logger = make_logger(name="get_all_counterparties_logs")


def get_all_counterparties(environment: str, username: str, password: str) -> requests.Response:
    if environment == "uat" or environment == "preprod":
        URL = f"https://{environment}.tradias.link"
    elif environment == "production":
        URL = "https://www.tradias.link"
    else: 
        raise EnvironmentError
    logger.info(f"Querying counterparty ID for {environment}")
    secret=get_login_token(base_url=URL, username=username, password=password)
    path = f"/api/counter_parties/names"
    headers = {"Authorization": f"Bearer {secret}"}
    response = requests.get(url=URL+path, headers=headers)
    logger.info(f"Received a {response.status_code}")
    return response



if __name__ == "__main__":
    from app.config.local_config import ANNE
    all_counterparties = get_all_counterparties(environment="production", 
                                                 username=ANNE.username_production, 
                                                 password=ANNE.password_production).json()
    for counterparty in all_counterparties["items"]:
        if "sygnum" in counterparty["name"].lower():
            print(f"Sygnum's ID is {counterparty['id']} for {counterparty['name']}")
        elif "amina" in counterparty["name"].lower():
            print(f"Amina's ID is {counterparty['id']} for {counterparty['name']}")
        elif "tradias" in counterparty["name"].lower():
            print(f"Tradias' ID is {counterparty['id']} for {counterparty['name']}")
            
            