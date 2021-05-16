import os
from .base import Notifier

import smtplib

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


class Gmail(Notifier):
    def notify(self, to, msg):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            msg = 'Covid slots available'
            msg = f"Subject: {msg} \n\n {msg}"
            smtp.sendmail(from_addr=EMAIL_ADDRESS, to_addrs="niteshrawat99@gmail.com", msg=msg)
