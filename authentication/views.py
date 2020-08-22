import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View


# class UsernameValidationView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         username = data["username"]
#         if not str(username).isalnum():
#             return JsonResponse(
#                 {"username_error": "Username should contain alphanumerics"}
#             )
#         return JsonResponse({"username_valid": True})
@csrf_exempt
def username_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {"username_error": "username should contain only alphanumerics"},
                status=400,
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "sorry the username is already in use"}, status=400,
            )

        return JsonResponse({"username_valid": True}, status=200)


def register(request):
    context = {}
    return render(request, "authentication/register.html", context)


@csrf_exempt
def username_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {"username_error": "username should contain only alphanumerics"},
                status=400,
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "sorry the username is already in use"}, status=400,
            )

        return JsonResponse({"username_valid": True}, status=200)

