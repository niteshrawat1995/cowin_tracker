import os
from .base import Notifier

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class Twilio(Notifier):
    TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
    FROM_WHATSAPP_NUMBER = os.environ.get("FROM_WHATSAPP_NUMBER")
    FROM_SMS_NUMBER = os.environ.get("FROM_SMS_NUMBER")
    TO_NUMBER = os.environ.get("TO_NUMBER")

    def __init__(self):
        self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        self.to_number = self.TO_NUMBER

    def send_whatsapp(self, msg):
        from_number = self.FROM_WHATSAPP_NUMBER
        to_number = f"whatsapp:{self.to_number}"
        print("Sending whatsapp")
        self._send(from_number, to_number, msg)
        
    def send_sms(self, msg):
        from_number = self.FROM_SMS_NUMBER
        to_number = self.to_number
        print("Sending sms")
        self._send(from_number, to_number, msg)

    def _send(self, from_number, to_number, msg):
        message = self.client.messages.create(
            body=msg, from_=from_number, to=to_number
        )
        print(message.sid)

    def notify(self, to, msg):
        self.send_whatsapp(msg=msg)
        self.send_sms(msg=msg)
