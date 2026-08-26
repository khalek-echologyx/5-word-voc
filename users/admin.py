from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_id",
        "created_at",
    )

    search_fields = ("device_id",)