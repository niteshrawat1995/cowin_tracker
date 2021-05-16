from test import BASE_DIR
from dateutil.parser import parse
from pathlib import Path
from os import path

BASE_DIR = Path(__file__).resolve().parent


def save_dt(date):
    date_str = str(date)
    file_path = path.join(BASE_DIR, "datefile.txt")
    with open(file_path, "w") as f:
        f.write(date_str)
    return True


def read_dt():
    file_path = path.join(BASE_DIR, "datefile.txt")
    with open(file_path, "r") as f:
        date_str = f.read()
    return parse(date_str)
