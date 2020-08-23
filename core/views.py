from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CountryData


@login_required
def index(request):
    all_data = CountryData.objects.all()
    most_cases = CountryData.objects.order_by("-total_cases")[:5]
    most_deaths = CountryData.objects.order_by("-total_deaths")[:5]
    context = {
        "all_data": all_data,
        "most_cases": most_cases,
        "most_deaths": most_deaths,
    }
    return render(request, "core/index.html", context)

