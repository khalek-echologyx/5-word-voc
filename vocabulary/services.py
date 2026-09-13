from django.utils import timezone

from ai.gemini import generate_and_save_words
from .models import DailyVocabulary


def generate_daily_words():
    today = timezone.localdate()

    daily_vocabulary = DailyVocabulary.objects.filter(
        date=today
    ).first()

    if daily_vocabulary:
        return daily_vocabulary

    words = generate_and_save_words()

    if len(words) != 5:
        raise ValueError(
            f"Expected 5 words, but received {len(words)}."
        )

    daily_vocabulary = DailyVocabulary.objects.create(
        date=today
    )

    daily_vocabulary.words.set(words)

    return daily_vocabulary