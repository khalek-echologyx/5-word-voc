from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyLesson
from .serializers import DailyLessonSerializer


class TodayLessonView(APIView):
    def get(self, request):
        today = timezone.localdate()

        lesson = DailyLesson.objects.filter(
            date=today,
            status=DailyLesson.Status.PUBLISHED,
        ).first()

        if not lesson:
            return Response(
                {
                    "detail": "Today's lesson is not available."
                },
                status=404,
            )

        serializer = DailyLessonSerializer(lesson)

        return Response(serializer.data)