from django.contrib import admin

from .models import Vocabulary


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "part_of_speech",
        "difficulty",
        "category",
        "source",
        "created_at",
    )

    search_fields = (
        "word",
        "bangla_meaning",
        "category",
    )

    list_filter = (
        "difficulty",
        "part_of_speech",
        "source",
    )