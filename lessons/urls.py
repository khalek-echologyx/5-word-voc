from django.urls import path

from .views import TodayLessonView


urlpatterns = [
    path(
        "today/",
        TodayLessonView.as_view(),
        name="today-lesson",
    ),
]