from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    register,
    today_vocabulary,
    open_today_vocabulary,
    today_vocabulary_status,
    logout,
    me,
    forgot_password,
    reset_password,
)


urlpatterns = [
    path(
        "today/",
        today_vocabulary,
        name="today-vocabulary",
    ),
    path(
        "today/open/",
        open_today_vocabulary,
        name="open-today-vocabulary",
    ),
    path(
        "today/status/",
        today_vocabulary_status,
        name="today-vocabulary-status",
    ),
    path(
        "login/",
        obtain_auth_token,
        name="login",
    ),
    path(
        "auth/register/",
        register,
        name="register",
    ),
    path(
        "auth/logout/",
        logout,
        name="logout",
    ),
    path(
        "auth/me/",
        me,
        name="me",
    ),
    path(
        "auth/forgot-password/",
        forgot_password,
        name="forgot-password",
    ),
    path(
        "auth/reset-password/",
        reset_password,
        name="reset-password",
    ),
]