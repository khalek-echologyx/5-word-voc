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