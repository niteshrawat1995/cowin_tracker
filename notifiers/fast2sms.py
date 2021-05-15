import os
from .base import Notifier

import requests

from dotenv import load_dotenv
load_dotenv()


class Fast2Sms(Notifier):
    API_KEY = os.environ.get("API_KEY_FAST2SMS")

    def notify(self, to, msg):
        url = "https://www.fast2sms.com/dev/bulkV2"

        payload = f"message={msg}&language=english&route=q&numbers={to}"
        headers = {
            'authorization': self.API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
