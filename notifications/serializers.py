import datetime

from rest_framework import serializers

from .models import NotificationSettings


class NotificationSettingsSerializer(serializers.ModelSerializer):
    """Serializer for reading and updating notification preferences."""

    notification_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M", "%H:%M:%S"],
        default=datetime.time(8, 0),
    )

    class Meta:
        model = NotificationSettings
        fields = [
            "is_enabled",
            "notification_time",
            "timezone",
            "push_token",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]


class PushTokenSerializer(serializers.Serializer):
    """Serializer for registering or updating the Expo push token."""

    push_token = serializers.CharField(max_length=500)
    timezone = serializers.CharField(max_length=100, required=False)
