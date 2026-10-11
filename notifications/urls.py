from django.urls import path

from .views import notification_settings, register_push_token

urlpatterns = [
    path(
        "settings/",
        notification_settings,
        name="notification-settings",
    ),
    path(
        "token/",
        register_push_token,
        name="register-push-token",
    ),
]
