from rest_framework import serializers
from django.contrib.auth.models import User
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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )