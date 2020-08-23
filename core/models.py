from django.db import models


class CountryData(models.Model):
    iso_code = models.CharField(max_length=5)
    continent = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    total_cases = models.FloatField()
    new_cases = models.FloatField()
    total_deaths = models.FloatField()

    def __str__(self):
        return self.location
