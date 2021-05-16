import datetime
import time
import requests
from typing import List
import notifiers

from notifiers.base import Notifier
from notifiers import CLICKSEND, GMAIL, LINUX, config, TWILIO, FAST2SMS
from utils import read_dt, save_dt

COWIN_BOOKING_SITE = "https://selfregistration.cowin.gov.in/"


def get_available_slots(pincodes: List[int], min_age_limit: int) -> List:
    now = datetime.date.today()
    date_str = now.strftime("%d-%m-%Y") 
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    headers = {
        'Content-Type': 'application/json', 'Accept-Language' : 'hi_IN' , 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    available_slots = []
    for pincode in pincodes:
        response = requests.get(url, params={"pincode": pincode, "date": date_str}, headers=headers)
        if response.status_code != 200:
            print(f"Cannot call API | ErrorCode: {response.status_code} | Response {response.content}")
            continue
        data = response.json()
        for center in data["centers"]:
            center_name = center["name"]
            center_address = center["address"]
            for session in center["sessions"]:
                available_capacity = session["available_capacity"]
                vaccine = session["vaccine"]
                date = session["date"]
                available_capacity = session["available_capacity"]
                if session["min_age_limit"] == min_age_limit  and available_capacity >= 5:
                    information = {
                        "center_name": center_name,
                        "center_address": center_address,
                        "available_capacity": available_capacity,
                        "vaccine": vaccine,
                        "date": date,
                    }
                    available_slots.append(information)
    return available_slots

def msg_builder(data) -> str:
    msg = ""
    # for d in data:
    #     center_name = d["center_name"]
    #     center_address = d["center_address"]
    #     available_capacity = d["available_capacity"]
    #     vaccine = d["vaccine"]
    #     date = d["date"]
    #     row_msg = f"{center_name} | {center_address} | {date} |{available_capacity} | {vaccine} \n"
    #     msg += row_msg
    # msg += f" Go visit: {COWIN_BOOKING_SITE}"
    # return msg
    # bigger msgs are actually multiple messages combined which will cost you more.
    msg = "Rawat Parlour Open Now !"
    return msg

def main(notifiers: List[Notifier], debug=True):

    def _run(notifiers: List[Notifier]):
        slots = get_available_slots(pincodes=[201301, 110076, 110096], min_age_limit=18)
        last_send_date = read_dt()
        current_dt = datetime.datetime.now()
        last_send_timedelta = current_dt - last_send_date
        last_send_minutes = last_send_timedelta.total_seconds() / 60
        if slots and last_send_minutes >= 30:
            # send notification and update last send date
            msg = msg_builder(slots)
            for notifier in notifiers:
                notifier.notify(to="7503437728", msg=msg)
            save_dt(current_dt)
        else:
            print(f"Notifiation NOT send | slots {len(slots)} | duration {last_send_minutes} mins")

    if debug:
        _run(notifiers=notifiers)
    else:
        # set the script in cron for every minute (* * * * *) and then excecute the script in gap of 10 seconds 6 times
        # not the best solution but, whatever.
        for _ in range(6):
            _run(notifiers=notifiers)
            # sleeping for 10 secs
            time.sleep(10)

if __name__ == "__main__":
    notifiers = [config[FAST2SMS](), config[LINUX](), config[CLICKSEND](), config[GMAIL]()]
    main(notifiers, debug=False)
