from django.contrib import admin

from .models import NotificationSendLog, NotificationSettings


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_enabled",
        "notification_time",
        "timezone",
        "push_token",
        "updated_at",
    )
    list_filter = ("is_enabled",)
    search_fields = ("user__username", "push_token")
    readonly_fields = ("created_at", "updated_at")


@admin.register(NotificationSendLog)
class NotificationSendLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "sent_at")
    list_filter = ("date",)
    search_fields = ("user__username",)
    readonly_fields = ("sent_at",)