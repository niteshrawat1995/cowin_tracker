import os
from twilio.rest import Client
import datetime
import requests
from typing import List
import time

from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.environ.get("FROM_WHATSAPP_NUMBER")
FROM_SMS_NUMBER = os.environ.get("FROM_SMS_NUMBER")
TO_NUMBER = os.environ.get("TO_NUMBER")

COWIN_BOOKING_SITE = "https://selfregistration.cowin.gov.in/"

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


def get_available_slots(pincode: int, min_age_limit: int) -> List:
    now = datetime.date.today()
    date_str = now.strftime("%d-%m-%Y") 
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    headers = {
        'Content-Type': 'application/json', 'Accept-Language' : 'hi_IN' , 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    response = requests.get(url, params={"pincode": pincode, "date": date_str}, headers=headers)
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
            vaccine = session["vaccine"]
            date = session["date"]
            available_capacity = session["available_capacity"]
            if session["min_age_limit"] == min_age_limit  and available_capacity > 0:
                information = {
                    "center_name": center_name,
                    "center_address": center_address,
                    "available_capacity": available_capacity,
                    "vaccine": vaccine,
                    "date": date,
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
        date = d["date"]
        row_msg = f"{center_name} | {center_address} | {date} |{available_capacity} | {vaccine} \n"
        msg += row_msg
    msg += f" Go visit: {COWIN_BOOKING_SITE}"
    return msg

def main(event=None, context=None):
    # set the script in cron for every minute (* * * * *) and then excecute the script in gap of 10 seconds 6 times
    # not the best solution but, whatever.
    for _ in range(6):     
        slots = get_available_slots(pincode=201301, min_age_limit=18)
        if slots:
            msg = msg_builder(slots)
            twilio = Twilio()
            twilio.send_whatsapp(msg)
            twilio.send_sms(msg)
        # sleeping for 10 secs
        time.sleep(10)

if __name__ == "__main__":
    main()
