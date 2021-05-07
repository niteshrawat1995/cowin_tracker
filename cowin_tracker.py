import os
from twilio.rest import Client
import datetime
import requests
import json
from typing import List

from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.environ.get("FROM_WHATSAPP_NUMBER")
FROM_SMS_NUMBER = os.environ.get("FROM_SMS_NUMBER")
TO_NUMBER = os.environ.get("TO_NUMBER")

class Twilio:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.to_number = TO_NUMBER

    def send_whatsapp(self, msg):
        from_number = FROM_WHATSAPP_NUMBER
        to_number = f"whatsapp:{self.to_number}"
        print("Sending whatsapp")
        self._send(from_number, to_number, msg)
        
    def send_sms(self, msg):
        from_number = FROM_SMS_NUMBER
        to_number = self.to_number
        print("Sending sms")
        self._send(from_number, to_number, msg)

    def _send(self, from_number, to_number, msg):
        message = self.client.messages.create(
            body=msg, from_=from_number, to=to_number
        )
        print(message.sid)


def get_available_slots() -> List:
    now = datetime.date.today()
    date_str = now.strftime("%d-%m-%Y") 
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    headers = {
        'Content-Type': 'application/json', 'Accept-Language' : 'hi_IN' , 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    response = requests.get(url, params={"pincode": 201301, "date": date_str}, headers=headers)
    if response.status_code != 200:
        print(f"Cannot call API | ErrorCode: {response.status_code} | Response {response.content}")
        return []
    data = response.json()
    information_list = []
    for center in data["centers"]:
        center_name = center["name"]
        center_address = center["address"]
        for session in center["sessions"]:
            available_capacity = session["available_capacity"]
            min_age_limit = session["min_age_limit"]
            vaccine = session["vaccine"]
            available_capacity = session["available_capacity"]
            if 18 <= min_age_limit < 45 and available_capacity > 0:
                information = {
                    "center_name": center_name,
                    "center_address": center_address,
                    "available_capacity": available_capacity,
                    "vaccine": vaccine
                }
                information_list.append(information)
    return information_list

def msg_builder(data) -> str:
    msg = ""
    for d in data:
        center_name = d["center_name"]
        center_address = d["center_address"]
        available_capacity = d["available_capacity"]
        vaccine = d["vaccine"]
        row_msg = f"{center_name} | {center_address} | {available_capacity} | {vaccine} \n"
        msg += row_msg
    return msg

def main(event=None, context=None):
    slots = get_available_slots()
    if slots:
        msg = msg_builder(slots)
        twilio = Twilio()
        twilio.send_whatsapp(msg)
        twilio.send_sms(msg)

if __name__ == "__main__":
    main()
