import os
from notifiers.base import Notifier

import messagebird
from dotenv import load_dotenv
load_dotenv()


class MessageBird(Notifier):
    API_KEY = os.environ.get("API_KEY_MESSAGEBIRD")

    def __init__(self) -> None:
        self.client = messagebird.Client(access_key=self.API_KEY)

    def notify(self, to, msg):
        message = self.client.message_create(
            originator="MessageBird", 
            recipients="+917503437728", 
            body="Test message from messagebird", 
            params={"reference": "Foobar"}
        )
        print(message.id)

mb = MessageBird()
mb.notify(1,1)