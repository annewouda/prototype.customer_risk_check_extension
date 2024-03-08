import requests 
import datetime

from app.config.local_config import WEBHOOK_URL

def send_webhook_message(message: str):
    body = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "RiskAlert triggered",
        "sections": [{
            "activityTitle": "Alart details",
            "activitySubtitle": str(datetime.datetime.utcnow()),
            "activityImage": "",
            "facts": [{
                "name": "Message:",
                "value": message
            }],
            "markdown": True
            }]
        }
    
    requests.post(url=WEBHOOK_URL, json=body)