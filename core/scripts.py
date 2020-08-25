import pandas as pd
import json
from datetime import datetime


def get_data():
    # convert dates in csv to datetime
    with open("./owid-covid-data.json") as f:
        covid_data = json.load(f)

    # create a subset of covid data
    country_names = []

    for data in covid_data:
        location = data["location"]
        code = data["iso_code"]
        value = data["total_deaths"]
        print(location)

        # country_names.append(location)

