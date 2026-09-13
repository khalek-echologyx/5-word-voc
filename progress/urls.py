from django.urls import path

from .views import (
    CompleteTodayLessonView,
    UserProgressView,
)


urlpatterns = [
    path(
        "complete/",
        CompleteTodayLessonView.as_view(),
        name="complete-today-lesson",
    ),
    path(
        "",
        UserProgressView.as_view(),
        name="user-progress",
    ),
]