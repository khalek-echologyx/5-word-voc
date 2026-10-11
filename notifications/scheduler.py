"""
APScheduler-based daily push notification job.

The scheduler is started inside NotificationsConfig.ready() so it runs
automatically when Django starts (both `runserver` and production WSGI/ASGI).

Design:
- A cron job fires every minute.
- For each user whose preferred local time matches the current UTC minute,
  the job checks NotificationSendLog to prevent duplicate sends.
- It batches Expo push messages and handles DeviceNotRegistered errors.
"""
import datetime
import logging

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db import IntegrityError
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger(__name__)

NOTIFICATION_TITLE = "5 Words Per Day 📚"
NOTIFICATION_BODY = (
    "Your 5 new English words are ready! Start learning today."
)


def send_daily_notifications():
    """
    Called every minute by APScheduler.

    Finds every user whose notification_time (in their local timezone)
    matches the current UTC time (to the minute), verifies they haven't
    already received a notification today (in their local date), and
    dispatches via the Expo Push API.
    """
    # Import here to avoid circular imports at module level
    from .expo import is_invalid_token_error, send_expo_push_notifications
    from .models import NotificationSendLog, NotificationSettings

    now_utc = datetime.datetime.now(tz=datetime.timezone.utc)

    enabled_settings = NotificationSettings.objects.filter(
        is_enabled=True,
    ).exclude(push_token="").select_related("user")

    if not enabled_settings.exists():
        return

    # Build a list of (settings_obj, local_date) pairs whose time matches now.
    to_notify = []

    for ns in enabled_settings:
        try:
            tz = pytz.timezone(ns.timezone)
        except pytz.UnknownTimeZoneError:
            logger.warning(
                "Unknown timezone '%s' for user %s — skipping.",
                ns.timezone,
                ns.user.username,
            )
            continue

        now_local = now_utc.astimezone(tz)
        local_date = now_local.date()

        # Match hour and minute only (scheduler fires every minute).
        if (
            now_local.hour == ns.notification_time.hour
            and now_local.minute == ns.notification_time.minute
        ):
            # Guard against duplicates: skip if already sent today
            # (local date in the user's timezone).
            already_sent = NotificationSendLog.objects.filter(
                user=ns.user,
                date=local_date,
            ).exists()

            if not already_sent:
                to_notify.append((ns, local_date))

    if not to_notify:
        return

    logger.info(
        "Sending daily notifications to %d user(s).", len(to_notify)
    )

    # Build Expo message batch.
    messages = [
        {
            "to": ns.push_token,
            "title": NOTIFICATION_TITLE,
            "body": NOTIFICATION_BODY,
            "sound": "default",
            "data": {"screen": "Home"},  # picked up by the mobile tap handler
        }
        for ns, _ in to_notify
    ]

    try:
        receipts = send_expo_push_notifications(messages)
    except RuntimeError:
        # HTTP-level failure; will retry next minute naturally.
        logger.error("Push batch failed; will retry next minute.")
        return

    # Process receipts: record successes, clear invalid tokens.
    for index, (ns, local_date) in enumerate(to_notify):
        receipt = receipts[index] if index < len(receipts) else {}

        if is_invalid_token_error(receipt):
            logger.warning(
                "DeviceNotRegistered for user %s — clearing token.",
                ns.user.username,
            )
            ns.push_token = ""
            ns.save(update_fields=["push_token", "updated_at"])
            continue

        if receipt.get("status") == "error":
            logger.error(
                "Push error for user %s: %s",
                ns.user.username,
                receipt.get("message", "unknown error"),
            )
            # Don't log a send record — let it retry next day.
            continue

        # Record successful send to prevent duplicates.
        try:
            NotificationSendLog.objects.create(
                user=ns.user,
                date=local_date,
            )
        except IntegrityError:
            # Race condition: another process already logged this. Safe to ignore.
            pass


def start_scheduler():
    """
    Start the APScheduler background scheduler with a Django database job store.
    The cron trigger fires once per minute so we can match user-preferred times.
    """
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_daily_notifications,
        trigger=CronTrigger(minute="*"),  # every minute, every hour
        id="send_daily_notifications",
        max_instances=1,
        replace_existing=True,
    )

    logger.info("APScheduler started — daily notification job registered.")
    scheduler.start()
