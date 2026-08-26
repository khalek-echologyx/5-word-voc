from django.db import models

from users.models import User
from lessons.models import DailyLesson


class DailyCompletion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="completions",
    )

    daily_lesson = models.ForeignKey(
        DailyLesson,
        on_delete=models.CASCADE,
        related_name="completions",
    )

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "daily_lesson"],
                name="unique_user_lesson_completion",
            ),
        ]

    def __str__(self):
        return f"{self.user.device_id} - {self.daily_lesson.date}"