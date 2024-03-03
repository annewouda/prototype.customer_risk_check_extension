import requests
    
from app.tools.get_access_token import get_login_token
from app.tools.make_logger import make_logger    
    

logger = make_logger(name="get_counterparty_balance_by_id_logs")
    
    
def get_counterparty_balances_by_id(environment: str, username: str, password: str, counterparty_id: str, query_params: dict):
    if environment == "uat" or environment == "preprod":
        URL = f"https://{environment}.tradias.link"
    elif environment == "production":
        URL = "https://www.tradias.link"
    else: 
        raise EnvironmentError
    logger.info(f"Getting balance on {environment} environment")
    path = f"/api/counter_parties/{counterparty_id}/balances?" + query_params
    logger.info(f"Quering with query parameters {query_params}")
    secret = get_login_token(base_url=URL, username=username, password=password)
    headers = {"Authorization": f"Bearer {secret}"}
    response = requests.get(url=URL+path, headers=headers)
    logger.info(f"Response from querying balance is {response.status_code}")
    return response



if __name__ == "__main__":
    from app.config.local_config import ANNE
    print(get_counterparty_balances_by_id(environment="production", 
                                          username=ANNE.username_production,
                                          password=ANNE.password_production,
                                          counterparty_id="fb1e14f1-6c06-4e29-ba57-8bd33f8521ab",
                                          query_params="currency_code=BTC").json())
    