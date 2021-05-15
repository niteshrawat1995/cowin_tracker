import os
from .base import Notifier

import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("FAST2SMS_API_KEY") 

class Fast2Sms(Notifier):
    def notify(self, to, msg):
        url = "https://www.fast2sms.com/dev/bulkV2"

        payload = f"message={msg}&language=english&route=q&numbers={to}"
        headers = {
            'authorization': API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
