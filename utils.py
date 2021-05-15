from dateutil.parser import parse


def save_dt(date):
    date_str = str(date)
    with open("datefile.txt", "w") as f:
        f.write(date_str)
    return True


def read_dt():
    with open("datefile.txt", "r") as f:
        date_str = f.read()
    return parse(date_str)
