from django.db import models


class DailyLesson(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    date = models.DateField(unique=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lesson - {self.date}"
    
from vocabulary.models import Vocabulary


class DailyLessonWord(models.Model):
    daily_lesson = models.ForeignKey(
        DailyLesson,
        on_delete=models.CASCADE,
        related_name="lesson_words",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="lesson_entries",
    )

    position = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["daily_lesson", "position"],
                name="unique_lesson_word_position",
            ),
            models.UniqueConstraint(
                fields=["daily_lesson", "vocabulary"],
                name="unique_vocabulary_per_lesson",
            ),
        ]

        ordering = ["position"]

    def __str__(self):
        return f"{self.daily_lesson.date} - {self.position}: {self.vocabulary.word}"