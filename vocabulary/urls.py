from django.urls import path

from .views import today_vocabulary


urlpatterns = [
    path("today/", today_vocabulary, name="today-vocabulary"),
]