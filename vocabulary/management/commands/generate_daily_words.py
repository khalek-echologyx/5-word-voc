from django.core.management.base import BaseCommand

from vocabulary.services import generate_daily_words


class Command(BaseCommand):
    help = "Generate and save today's 5 vocabulary words"

    def handle(self, *args, **options):
        daily_vocabulary = generate_daily_words()

        word_count = daily_vocabulary.words.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Today's vocabulary is ready: {word_count} words."
            )
        )