from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CountryData


@login_required
def index(request):
    all_data = CountryData.objects.all().distinct()[:10]
    most_cases = CountryData.objects.order_by("-total_cases")[:5]
    most_deaths = CountryData.objects.order_by("-total_deaths")[:20]
    paginator = Paginator(all_data, 5)
    paginator2 = Paginator(most_deaths, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    page_obj_2 = Paginator.get_page(paginator2, page_number)
    context = {
        "all_data": all_data,
        "most_cases": most_cases,
        "most_deaths": most_deaths,
        "page_obj": page_obj,
        "page_obj_2": page_obj_2,
    }
    return render(request, "core/index.html", context)

