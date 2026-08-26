from django.contrib import admin

from .models import DailyCompletion


@admin.register(DailyCompletion)
class DailyCompletionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "daily_lesson",
        "completed_at",
    )

    list_filter = ("daily_lesson",)