import requests

from app.tools.make_logger import make_logger
from app.models.counterparty import CounterParty
from app.controllers.get_counterparty_balance_by_id import get_counterparty_balances_by_id
from app.controllers.communication_api_controller import communication_api_controller

from app.config.local_config import ANNE
from app.config.counterparties import AMINA, SYGNUM
from app.config.recipients import target_phone_call_numbers, target_email_recipients, target_text_message_numbers, error_phone_call_numbers, error_text_message_numbers
from app.controllers.send_webhook_message import send_webhook_message


logger = make_logger(name="lambda_function_logs")


counterparties=[AMINA, SYGNUM]
username=ANNE.username_production
password=ANNE.password_production


def lambda_handler(event: dict, context: dict):
        balances = {}
        error_messages = []
        try:
                for counterparty in counterparties:
                        balances[counterparty.name] = {}
                        counterparty_id = counterparty.id
                        for currency in counterparty.limits_per_currency.keys():
                                query_params = "currency_code=" + currency
                                balance_response = get_counterparty_balances_by_id(environment="production",
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
                                        message = f"Risk breach for {counterparty.name} in {currency} of {balance}, the actual limit is {limit}. Balance is at {round(absolute_balance/limit,2)} times the limit."
                                        error_messages.append(message)

                if error_messages:
                        message = ", ".join(error_messages)
                        communication_api_controller(endpoint="https://communication-api.tradias.de",
                                                     phone_numbers=target_phone_call_numbers,
                                                     text_msg_numbers=target_text_message_numbers,
                                                     email_addresses=target_email_recipients,
                                                     phone_message=message + "I repeat" + message,
                                                     text_message=message)
                        send_webhook_message(message=f"{message}. The balances are {balances}.")
                logger.info(f"The retrieved balances are {balances}")
        except Exception as e:
                message = f"Error {e} in customer risk check extension. I repeat, error {e} in customer risk check extension."
                communication_api_controller(endpoint="https://communication-api.tradias.de",
                                             phone_numbers=error_phone_call_numbers,
                                             text_msg_numbers=error_text_message_numbers,
                                             email_addresses=target_email_recipients,
                                             phone_message=message,
                                             text_message=message)
                logger.exception("Error in customer risk check extension.")

        
lambda_handler(event={}, context={})
        
        
        
# if __name__ == "__main__":
#         from app.config.local_config import ANNE
#         from app.config.counterparties import AMINA, SYGNUM
#         from app.config.recipients import target_phone_call_numbers, target_email_recipients, target_text_message_numbers
        
#         print(lambda_handler(event={},
#                              context={},
#                              counterparties=[AMINA, SYGNUM],
#                              username=ANNE.username_preprod,
#                              password=ANNE.password_preprod,
#                              target_phone_call_numbers=target_phone_call_numbers,
#                              target_text_msg_numbers=target_text_message_numbers,
#                              target_email_addresses=target_email_recipients))
        
        