import os
from .base import Notifier

import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException


class ClickSend(Notifier):
    USERNAME = os.environ.get("USERNAME_CLICKSEND")
    PASSWORD = os.environ.get("API_KEY_CLICKSEND")

    def __init__(self) -> None:
        configuration = clicksend_client.Configuration()
        configuration.username = self.USERNAME
        configuration.password = self.PASSWORD
        self.api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

    def notify(self, to, msg):
        sms_message = SmsMessage(source="python", body=msg, to=f"+91{to}")
        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
        try:
            # Send sms message(s)
            api_response = self.api_instance.sms_send_post(sms_messages)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
