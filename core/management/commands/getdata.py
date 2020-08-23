import os
import pandas as pd
import json
from django.core.management.base import BaseCommand
from datetime import datetime
from core.models import CountryData


class Command(BaseCommand):
    help = "Get data from CSV"

    def handle(self, *args, **kwargs):
        # convert dates in csv to datetime
        # d_parser = lambda x: datetime.strptime(x, "%Y-%m-%d")
        df = pd.read_csv("./owid-covid-data.csv")

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

        country_data.to_json("./owid-covid-data.json", orient="records")

        with open("./owid-covid-data.json") as f:
            covid_data = json.load(f)

        for data in covid_data:
            CountryData.objects.create(
                date=data["date"],
                iso_code=data["iso_code"],
                continent=data["continent"],
                location=data["location"],
                total_cases=data["total_cases"],
                new_cases=data["new_cases"],
                total_deaths=data["total_deaths"],
            )

        self.stdout.write("job complete")
