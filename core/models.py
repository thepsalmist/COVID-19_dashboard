from django.db import models


class CountryData(models.Model):
    iso_code = models.CharField(max_length=5, null=True)
    continent = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    total_cases = models.FloatField(null=True)
    new_cases = models.FloatField(null=True)
    total_deaths = models.FloatField(null=True)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = "CountryData"

