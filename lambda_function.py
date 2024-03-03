import requests

from app.tools.make_logger import make_logger
from app.models.counterparty import CounterParty
from app.controllers.get_counterparty_balance_by_id import get_counterparty_balances_by_id
from app.controllers.communication_api_controller import communication_api_controller


logger = make_logger(name="lambda_function_logs")


def lambda_handler(event: dict, context: dict, counterparties: list[CounterParty], username: str, password: str, target_phone_call_numbers: dict, target_email_addresses: dict, target_text_msg_numbers: dict):
        balances = {}
        for counterparty in counterparties:
                balances[counterparty.name] = {}
                counterparty_id = counterparty.id
                for currency in counterparty.limits_per_currency.keys():
                        query_params = "currency_code=" + currency
                        balance_response = get_counterparty_balances_by_id(environment="preprod",
                                                                           username=username,
                                                                           password=password,
                                                                           counterparty_id=counterparty_id,
                                                                           query_params=query_params
                                                                           ).json()
                        balance = balance_response["total_balance"]
                        balances[counterparty.name][currency] = balance
                        limit = counterparty.limits_per_currency[currency]
                        absolute_balance = abs(float(balance))
                        if absolute_balance > limit:
                                logger.info(f"RISK BREACH for {counterparty.name} in {currency}") 
                                #CALL THE COMMUNICATION API HERE
                                message = f"Risk breach for {counterparty.name} in {currency} of {balance}, the actual limit is {limit}. Balance is at {absolute_balance/limit} percent of the limit."
                                target_phone_call_numbers = target_phone_call_numbers
                                communication_api_controller(endpoint="https://communication-api.tradias.de",
                                                             phone_numbers=target_phone_call_numbers,
                                                             text_msg_numbers=target_text_msg_numbers,
                                                             email_addresses=target_email_addresses,
                                                             phone_message=message,
                                                             text_message=message)
        logger.info(f"The retrieved balances are {balances}")
        return balances
        
                        
        
        
        
if __name__ == "__main__":
        from app.config.local_config import ANNE
        from app.config.counterparties import AMINA, SYGNUM
        from app.config.recipients import target_phone_call_numbers, target_email_recipients, target_text_message_numbers
        
        print(lambda_handler(event={},
                             context={},
                             counterparties=[AMINA, SYGNUM],
                             username=ANNE.username_preprod,
                             password=ANNE.password_preprod,
                             target_phone_call_numbers=target_phone_call_numbers,
                             target_text_msg_numbers=target_text_message_numbers,
                             target_email_addresses=target_email_recipients))
        
        