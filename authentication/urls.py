from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = "authentication"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("validate_username/", views.username_validation, name="validate_username"),
    path("validate_email/", views.email_validation, name="validate_email"),
    # path(
    #     "validate_username/",
    #     csrf_exempt(UsernameValidationView.as_view()),
    #     name="validate_username",
    # ),
]
