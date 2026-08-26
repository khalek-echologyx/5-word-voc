from django.contrib import admin

from .models import DailyLesson, DailyLessonWord


class DailyLessonWordInline(admin.TabularInline):
    model = DailyLessonWord
    extra = 5
    min_num = 5
    max_num = 5


@admin.register(DailyLesson)
class DailyLessonAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    inlines = [DailyLessonWordInline]


@admin.register(DailyLessonWord)
class DailyLessonWordAdmin(admin.ModelAdmin):
    list_display = (
        "daily_lesson",
        "position",
        "vocabulary",
    )

    list_filter = ("daily_lesson",)