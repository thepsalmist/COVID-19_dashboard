import json
import os
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from .utils import token_generator


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
        if not validate_email(email, check_mx=True, check_regex=True):
            return JsonResponse(
                {"email_error": "The email format is invalid"}, status=400,
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "sorry the email already exists"}, status=400,
            )

        return JsonResponse({"email_valid": True}, status=200)


def register(request):
    """
    Register user
    """
    if request.method == "POST":
        # get user data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        # validation
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if password != password2:
                    messages.warning(request, "Passwords do not match")
                else:
                    new_user = User.objects.create_user(username=username, email=email)
                    new_user.set_password(password)
                    new_user.is_active = False
                    new_user.save()

                    # encode uid
                    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
                    # get secure token

                    # get domain
                    domain = get_current_site(request).domain
                    # relative url for emai activation
                    link = reverse(
                        "authentication:activate_account",
                        kwargs={
                            "uidb64": uidb64,
                            "token": token_generator.make_token(new_user),
                        },
                    )
                    activate_link = "http://" + domain + link
                    email_subject = "Activate your account"
                    email_body = (
                        "Hi "
                        + new_user.username
                        + " Welcome to Analytics. Use the link below to verify your email address \n"
                        + activate_link
                    )
                    sender_email = os.environ.get("DEFAULT_FROM_EMAIL")

                    email = EmailMessage(
                        email_subject, email_body, sender_email, [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(
                        request,
                        f"Account created succesfully for {new_user.username}, login to your email to verify account ",
                    )
                    return redirect("authentication:login")

    context = {"dataValues": request.POST}
    return render(request, "authentication/register.html", context)


def account_verification(request, uidb64, token):
    """
    Verify account via email, takes in base 64 user id and token
    Validates token and redirects user to login
    """
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        # check if user is already activated
        if not token_generator.check_token(user, token):
            return redirect("authentication:login")

        else:
            if user.is_active:
                return redirect("authentication:login")
            user.is_active = True
            user.save()
            messages.success(
                request, "Welcome! your account has been activated, proceed to login"
            )
            return redirect("authentication:login")

    except Exception as e:
        pass

    return redirect("authentication:login")


def login(request):
    """
    Login user. Checks if the credentials are valid, logs in user
    Redirecs to home page
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome to Analytica")
                    return redirect("core:home")
                messages.error(
                    request,
                    "Your account is not active, check your email to verify your account",
                )
                return render(request, "authentication/login.html")

        messages.warning(request, "Invalid credentials, please check again")
        return render(request, "authentication/login.html")

    context = {}
    return render(request, "authentication/login.html", context)


def logout(request):
    """
    Logout user
    """
    if request.method == "POST":
        auth.logout(request)
        return render(request, "authentication/logout.html", context={})

