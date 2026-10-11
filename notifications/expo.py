"""
Expo Push Notification service.

Sends notifications via the Expo Push API
(https://docs.expo.dev/push-notifications/sending-notifications/).
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

EXPO_PUSH_URL = getattr(
    settings, "EXPO_PUSH_URL", "https://exp.host/--/api/v2/push/send"
)


def send_expo_push_notifications(messages: list[dict]) -> list[dict]:
    """
    Send a batch of Expo push messages.

    Each message dict must contain at least:
        { "to": "ExponentPushToken[...]", "title": "...", "body": "..." }

    Returns the list of Expo receipt objects (one per message).
    Raises RuntimeError on HTTP-level failures.
    """
    if not messages:
        return []

    try:
        response = requests.post(
            EXPO_PUSH_URL,
            json=messages,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.RequestException as exc:
        logger.error("Expo push HTTP error: %s", exc)
        raise RuntimeError(f"Expo push request failed: {exc}") from exc


def is_invalid_token_error(receipt: dict) -> bool:
    """Return True when Expo reports the push token is no longer valid."""
    return (
        receipt.get("status") == "error"
        and receipt.get("details", {}).get("error") == "DeviceNotRegistered"
    )
