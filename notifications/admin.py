from django.contrib import admin

from .models import NotificationSettings


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_enabled",
        "notification_time",
        "timezone",
    )

    list_filter = ("is_enabled", "timezone")