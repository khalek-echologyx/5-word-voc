from django.db import models

from users.models import User


class NotificationSettings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )

    is_enabled = models.BooleanField(default=True)

    notification_time = models.TimeField(
        null=True,
        blank=True,
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Dhaka",
    )

    push_token = models.CharField(
        max_length=500,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification settings - {self.user.device_id}"