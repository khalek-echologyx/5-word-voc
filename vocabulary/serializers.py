from rest_framework import serializers

from .models import Vocabulary, DailyVocabulary


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = [
            "id",
            "word",
            "pronunciation",
            "part_of_speech",
            "bangla_meaning",
            "definition",
            "example_sentence",
            "difficulty",
            "category",
        ]


class DailyVocabularySerializer(serializers.ModelSerializer):
    words = VocabularySerializer(many=True, read_only=True)

    class Meta:
        model = DailyVocabulary
        fields = [
            "id",
            "date",
            "words",
        ]