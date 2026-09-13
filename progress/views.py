from progress.serializers import UserProgressSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import DailyLesson
from users.models import User

from .models import DailyCompletion


class CompleteTodayLessonView(APIView):
    def post(self, request):
        device_id = request.data.get("device_id")

        if not device_id:
            return Response(
                {
                    "detail": "device_id is required."
                },
                status=400,
            )

        user, created = User.objects.get_or_create(
            device_id=device_id
        )

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

        completion, created = DailyCompletion.objects.get_or_create(
            user=user,
            daily_lesson=lesson,
        )

        return Response(
            {
                "completed": True,
                "already_completed": not created,
                "completed_at": completion.completed_at,
            }
        )

class UserProgressView(APIView):
    def get(self, request):
        device_id = request.query_params.get("device_id")

        if not device_id:
            return Response(
                {
                    "detail": "device_id is required."
                },
                status=400,
            )

        user = User.objects.filter(
            device_id=device_id
        ).first()

        if not user:
            return Response(
                {
                    "total_days_completed": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                }
            )

        completions = DailyCompletion.objects.filter(
            user=user
        ).select_related("daily_lesson")

        completed_dates = sorted(
            completion.daily_lesson.date
            for completion in completions
        )

        total_days_completed = len(completed_dates)

        current_streak = 0
        longest_streak = 0

        if completed_dates:
            # Calculate longest streak
            streak = 1

            for index in range(1, len(completed_dates)):
                difference = (
                    completed_dates[index]
                    - completed_dates[index - 1]
                ).days

                if difference == 1:
                    streak += 1
                else:
                    streak = 1

                longest_streak = max(
                    longest_streak,
                    streak,
                )

            longest_streak = max(
                longest_streak,
                1,
            )

            # Calculate current streak
            today = timezone.localdate()

            if completed_dates[-1] == today:
                current_streak = 1

                for index in range(
                    len(completed_dates) - 1,
                    0,
                    -1,
                ):
                    difference = (
                        completed_dates[index]
                        - completed_dates[index - 1]
                    ).days

                    if difference == 1:
                        current_streak += 1
                    else:
                        break

        data = {
            "total_days_completed": total_days_completed,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        }

        serializer = UserProgressSerializer(data)

        return Response(serializer.data)
    def get(self, request):
        device_id = request.query_params.get("device_id")

        if not device_id:
            return Response(
                {
                    "detail": "device_id is required."
                },
                status=400,
            )

        user = User.objects.filter(
            device_id=device_id
        ).first()

        if not user:
            return Response(
                {
                    "total_days_completed": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                }
            )

        completions = DailyCompletion.objects.filter(
            user=user
        )

        total_days_completed = completions.count()

        data = {
            "total_days_completed": total_days_completed,
            "current_streak": 0,
            "longest_streak": 0,
        }

        serializer = UserProgressSerializer(data)

        return Response(serializer.data)