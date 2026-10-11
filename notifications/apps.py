import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NotificationsConfig(AppConfig):
    name = "notifications"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """
        Start the background scheduler when Django initialises.

        Guards against double-start (which can happen with runserver's
        auto-reloader spawning a child process) by catching the
        SchedulerAlreadyRunningError.
        """
        import os

        # Only start in the main process; Django's autoreloader spawns a child
        # with RUN_MAIN=true. Skip the parent process to avoid double-start.
        if os.environ.get("RUN_MAIN") == "true" or not os.environ.get(
            "RUN_MAIN"
        ):
            try:
                from .scheduler import start_scheduler

                start_scheduler()
            except Exception as exc:  # pragma: no cover
                logger.error("Failed to start notification scheduler: %s", exc)
