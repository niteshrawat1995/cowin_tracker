from .base import Notifier

import requests

API_KEY = "Kdt5FjI4QfU7HpaJAkGMg6WRble3czLy0Nsq2DVZirYwTuCxmO1gcR4hy697NdtJuHZpIs3kqBj2Tboe"


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
