from django.contrib import admin
from .models import CountryData


@admin.register(CountryData)
class CountryDataAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "iso_code",
        "continent",
        "location",
        "total_cases",
        "new_cases",
        "total_deaths",
    ]
    list_filter = ["continent", "location", "date"]
    search_fields = ["continent", "location"]
    ordering = ["-location"]

