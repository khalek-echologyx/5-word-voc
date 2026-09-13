from rest_framework import serializers

from .models import DailyLesson, DailyLessonWord
from vocabulary.models import Vocabulary


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = [
            "word",
            "pronunciation",
            "part_of_speech",
            "bangla_meaning",
            "definition",
            "example_sentence",
            "difficulty",
            "category",
        ]


class DailyLessonWordSerializer(serializers.ModelSerializer):
    vocabulary = VocabularySerializer(read_only=True)

    class Meta:
        model = DailyLessonWord
        fields = [
            "position",
            "vocabulary",
        ]


class DailyLessonSerializer(serializers.ModelSerializer):
    words = serializers.SerializerMethodField()

    class Meta:
        model = DailyLesson
        fields = [
            "date",
            "status",
            "words",
        ]

    def get_words(self, obj):
        lesson_words = obj.lesson_words.all()

        return DailyLessonWordSerializer(
            lesson_words,
            many=True,
        ).data