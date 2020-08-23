import pandas as pd
import json
from datetime import datetime


def get_data():
    # convert dates in csv to datetime
    d_parser = lambda x: datetime.strptime(x, "%Y-%m-%d")
    df = pd.read_csv(
        "./owid-covid-data.csv", parse_dates=["date"], date_parser=d_parser
    )

    # create a subset of covid data
    country_data = df[
        [
            "date",
            "iso_code",
            "continent",
            "location",
            "total_cases",
            "new_cases",
            "total_deaths",
        ]
    ]

    country_data.to_json("./owid-covid-data.json", orient="records", lines=True)

