from django.db import models


class Vocabulary(models.Model):
    word = models.CharField(max_length=100)
    normalized_word = models.CharField(max_length=100, unique=True)

    pronunciation = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=50)

    bangla_meaning = models.CharField(max_length=255)
    definition = models.TextField()
    example_sentence = models.TextField()

    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=100)

    source = models.CharField(max_length=50, default="gemini")
    generated_by = models.CharField(max_length=100, blank=True)
    generation_version = models.CharField(max_length=50, default="v1")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word


class DailyVocabulary(models.Model):
    date = models.DateField(unique=True)
    words = models.ManyToManyField(
        Vocabulary,
        related_name="daily_vocabularies"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vocabulary for {self.date}"

class DailyVocabularyOpen(models.Model):
    daily_vocabulary = models.ForeignKey(
        DailyVocabulary,
        on_delete=models.CASCADE,
        related_name="opens",
    )

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="daily_vocabulary_opens",
    )

    opened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["daily_vocabulary", "user"],
                name="unique_daily_vocabulary_open",
            )
        ]

    def __str__(self):
        return f"{self.user} opened {self.daily_vocabulary.date}"