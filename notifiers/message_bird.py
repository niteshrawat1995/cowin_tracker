print(__name__)
from notifiers.base import Notifier

import messagebird

API_KEY = "kzz9xEpEmawjUgur16pFD9oRG"

class MessageBird(Notifier):

    def __init__(self) -> None:
        self.client = messagebird.Client(access_key=API_KEY)

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