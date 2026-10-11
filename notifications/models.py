import datetime

from django.contrib.auth.models import User
from django.db import models


class NotificationSettings(models.Model):
    """Stores per-user push notification preferences and Expo push token."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )

    is_enabled = models.BooleanField(default=True)

    # Default reminder time: 8:00 AM in the user's local timezone.
    notification_time = models.TimeField(
        default=datetime.time(8, 0),
    )

    # IANA timezone string (e.g. "Asia/Dhaka", "America/New_York").
    timezone = models.CharField(
        max_length=100,
        default="UTC",
    )

    # Expo push token for this device, e.g. "ExponentPushToken[...]".
    # Blank when the user has not granted notification permissions.
    push_token = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification Settings"
        verbose_name_plural = "Notification Settings"

    def __str__(self):
        return f"NotificationSettings – {self.user.username}"


class NotificationSendLog(models.Model):
    """
    Records every successfully dispatched daily notification.
    The unique constraint on (user, date) prevents duplicate sends
    for the same user on the same calendar date.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notification_send_logs",
    )

    # The calendar date (in the user's local timezone) for which this
    # notification was sent.
    date = models.DateField()

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_notification_per_user_per_day",
            )
        ]
        ordering = ["-sent_at"]

    def __str__(self):
        return f"Notification sent to {self.user.username} on {self.date}"