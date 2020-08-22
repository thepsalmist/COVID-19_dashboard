import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from validate_email import validate_email


# class UsernameValidationView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         username = data["username"]
#         if not str(username).isalnum():
#             return JsonResponse(
#                 {"username_error": "Username should contain alphanumerics"}
#             )
#         return JsonResponse({"username_valid": True})

# setup username validation
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


# setup email validation
@csrf_exempt
def email_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {"email_error": "The email format is invalid"}, status=400,
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "sorry the email already exists"}, status=400,
            )

        return JsonResponse({"email_valid": True}, status=200)


def register(request):
    context = {}
    return render(request, "authentication/register.html", context)

