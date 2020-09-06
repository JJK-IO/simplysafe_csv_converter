import os

import requests
from dotenv import load_dotenv
from pyrh import Robinhood


def convert_export_to_import(file_location, export_location=None):
    if not export_location:
        file_location_split = file_location.split("/")
        export_location = file_location_split[len(file_location_split) - 1].strip()
        export_location = f'converted-{export_location}'

    with open(file_location, "r") as f:
        data = f.readlines()

    with open(export_location, "w") as wf:
        for line in data:
            row = line.split(",")
            wf.write(f"{row[0]},{row[3]},{row[4]}\n")


def pull_from_rh():
    load_dotenv(verbose=True)
    rh_user = os.getenv("ROBINHOOD_USERNAME")
    rh_pass = os.getenv("ROBINHOOD_PASSWORD")
    rh_qr = os.getenv("ROBINHOOD_QR")
    rh = Robinhood()
    rh.login(username=rh_user, password=rh_pass, qr_code=rh_qr)

    positions = rh.positions()
    with open("rh_export.csv", "w") as wf:
        wf.write("Ticker,Shares,Cost Per Share\n")
        for position in positions["results"]:
            instrument = requests.get(position["instrument"])
            symbol = instrument.json()["symbol"]
            wf.write(f"{symbol},{position['quantity']},{position['average_buy_price']}\n")
        wf.flush()

    # print(rh.investment_profile())
    # print(json.dumps(rh.positions(), indent=2))
    # print(json.dumps(rh.securities_owned(), indent=2))
