from rest_framework import serializers

from .models import DailyCompletion


class DailyCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCompletion
        fields = [
            "daily_lesson",
            "completed_at",
        ]
        read_only_fields = [
            "completed_at",
        ]


class UserProgressSerializer(serializers.Serializer):
    total_days_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()