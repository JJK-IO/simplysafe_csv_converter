import errno
import os
from datetime import date

import requests
from dotenv import load_dotenv
from pyrh import Robinhood


def convert_export_to_import(file_location, export_location=None):
    if not export_location:
        file_location_split = file_location.split("/")
        export_location = (
            "".join(file_location_split[:-1])
            + file_location_split[len(file_location_split) - 1].strip()
        )
        export_location = f"converted-{export_location}"

    with open(file_location, "r") as f:
        data = f.readlines()

    with open(export_location, "w") as wf:
        for line in data:
            row = line.split(",")
            wf.write(f"{row[0]},{row[3]},{row[4]}\n")


def rh_setup():
    load_dotenv(verbose=True)
    rh_user = os.getenv("ROBINHOOD_USERNAME")
    rh_pass = os.getenv("ROBINHOOD_PASSWORD")
    rh_qr = os.getenv("ROBINHOOD_QR")
    rh = Robinhood()
    rh.login(username=rh_user, password=rh_pass, qr_code=rh_qr)

    return rh


def pull_from_rh(export_directory=None):
    if export_directory:
        if not os.path.exists(os.path.dirname(export_directory)):
            try:
                os.makedirs(os.path.dirname(export_directory))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    rh = rh_setup()
    securities = rh.securities_owned()
    with open(f"{export_directory}/rh_export_{date.today()}.csv", "w") as wf:
        wf.write("Ticker,Shares,Cost Per Share\n")
        for security in securities["results"]:
            instrument = requests.get(security["instrument"])
            symbol = instrument.json()["symbol"]
            wf.write(
                f"{symbol},{security['quantity']},{security['average_buy_price']}\n"
            )
        wf.flush()

    # print(rh.investment_profile())
    # print(json.dumps(rh.positions(), indent=2))
    # print(json.dumps(rh.securities_owned(), indent=2))


def security_list_from_rh():
    rh = rh_setup()
    securities = rh.securities_owned()
    security_list = []

    for security in securities["results"]:
        instrument = requests.get(security["instrument"])
        symbol = instrument.json()["symbol"]
        security_list.append(symbol)

    print(security_list)
