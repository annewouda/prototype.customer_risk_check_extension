from app.models.communication_api import CommunicationAPI
from app.config.local_config import PHONE_CALL_TOKEN, EMAIL_TOKEN, TEXT_MESSAGE_TOKEN

from app.tools.make_logger import make_logger


logger = make_logger(name="communication_api_controller_logs")


def communication_api_controller(endpoint: str, phone_numbers: dict, text_msg_numbers: dict, email_addresses: dict, phone_message: str, text_message: str):
    phone_call = CommunicationAPI(token=PHONE_CALL_TOKEN,
                                  endpoint=endpoint)
    email = CommunicationAPI(token=EMAIL_TOKEN,
                             endpoint=endpoint)
    send_text_message = CommunicationAPI(token=TEXT_MESSAGE_TOKEN,
                                         endpoint=endpoint)
    
        
    for phone_number in phone_numbers.values():
        phone_call.placecall(target_number=phone_number,
                             target_message=phone_message)   
        logger.info(f"Called {phone_number} with message {phone_message}")
        
    for person, email_address in email_addresses.items():
        email.sendemail(target_recipients=email_address,
                        subject="Risk Breach",
                        body_text=text_message)
        logger.info(f"Sent email to {person} at {email_address}, with message {text_message}")
    
    for person, phone_number in text_msg_numbers.items():
        send_text_message.sendtextmessage(target_number=phone_number,
                                          target_message=text_message,
                                          sender_id="Tradias Risk Info") 
        logger.info(f"Sent text to {person}, phone number {phone_number}, with message {text_message}")
        
        
        

if __name__ == "__main__":
    from app.config.recipients import target_phone_call_numbers, target_text_message_numbers, target_email_recipients
    
    communication_api_controller(endpoint="https://communication-api.tradias.de",
                                 phone_numbers=target_phone_call_numbers,
                                 text_msg_numbers=target_text_message_numbers,
                                 email_addresses=target_email_recipients,
                                 phone_message="Risk Test",
                                 text_message="Risk Test")
    
