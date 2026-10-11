import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import NotificationSettings
from .serializers import NotificationSettingsSerializer, PushTokenSerializer

logger = logging.getLogger(__name__)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def notification_settings(request):
    """
    GET  /api/notifications/settings/
        Returns the authenticated user's notification preferences.
        Creates a default record if one does not yet exist.

    PUT  /api/notifications/settings/
        Updates notification preferences (is_enabled, notification_time,
        timezone, push_token).  All fields are optional in a partial update.
    """
    settings_obj, _ = NotificationSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "GET":
        serializer = NotificationSettingsSerializer(settings_obj)
        return Response({"success": True, **serializer.data})

    # PUT — partial update so the client can send only changed fields
    serializer = NotificationSettingsSerializer(
        settings_obj,
        data=request.data,
        partial=True,
    )

    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer.save()
    return Response({"success": True, **serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_push_token(request):
    """
    POST /api/notifications/token/
        Body: { "push_token": "ExponentPushToken[...]", "timezone": "Asia/Dhaka" }

        Registers or updates the Expo push token for the authenticated user.
        Optionally updates the timezone at the same time.
        Creates the NotificationSettings record if it does not exist yet.
    """
    serializer = PushTokenSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    push_token = serializer.validated_data["push_token"]
    timezone = serializer.validated_data.get("timezone")

    settings_obj, _ = NotificationSettings.objects.get_or_create(
        user=request.user
    )

    settings_obj.push_token = push_token

    if timezone:
        settings_obj.timezone = timezone

    settings_obj.save(
        update_fields=["push_token", "timezone", "updated_at"]
        if timezone
        else ["push_token", "updated_at"]
    )

    logger.info(
        "Push token registered for user %s (timezone: %s)",
        request.user.username,
        settings_obj.timezone,
    )

    return Response(
        {
            "success": True,
            "message": "Push token registered successfully.",
        }
    )
