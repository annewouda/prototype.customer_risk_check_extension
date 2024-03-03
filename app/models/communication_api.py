import requests


class CommunicationAPI:
    def __init__(self, token, endpoint):
        self.token = token
        self.endpoint = endpoint
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _make_request(self, path, body):
        return requests.post(self.endpoint + path, headers=self.headers, json=body)

    def placecall(self,
                  target_number,
                  target_message):
        body = {
            "target_number": target_number,
            "target_message": target_message
        }
        return self._make_request("/placecall", body)

    def sendtextmessage(self,
                        target_number,
                        target_message,
                        sender_id = None):
        body = {
            "target_number": target_number,
            "target_message": target_message
        }
        if sender_id:
            body["sender_id"] = sender_id
        return self._make_request("/sendtextmessage", body)


    def sendemail(self,
                  target_recipients,
                  subject,
                  body_text,
                  body_html = None):

        body = {"target_recipients": target_recipients,
                "subject": subject,
                "body_text": body_text}
        if body_html:
            body["body_html"] = body_html
        return self._make_request("/sendemail", body)
    
