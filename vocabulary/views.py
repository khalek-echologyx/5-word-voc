from vocabulary.utils import api_error_response
import logging
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    DailyVocabularySerializer,
    RegisterSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .services import generate_daily_words
from .models import DailyVocabularyOpen
from .services import generate_daily_words

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import DailyVocabularyOpen


logger = logging.getLogger(__name__)

@api_view(["GET"])
def today_vocabulary(request):
    try:
        daily_vocabulary = generate_daily_words()

        serializer = DailyVocabularySerializer(daily_vocabulary)

        return Response({
            "success": True,
            **serializer.data,
        })

    except Exception:
        logger.exception(
            "Error while fetching today's vocabulary"
        )

        return api_error_response(
            "Unable to generate today's vocabulary."
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def open_today_vocabulary(request):
    try:
        daily_vocabulary = generate_daily_words()

        opened, created = DailyVocabularyOpen.objects.get_or_create(
            daily_vocabulary=daily_vocabulary,
            user=request.user,
        )

        return Response({
            "success": True,
            "opened": True,
            "already_opened": not created,
            "opened_at": opened.opened_at,
        })

    except Exception:
        return Response(
            {
                "success": False,
                "error": "Unable to record vocabulary open.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def today_vocabulary_status(request):
    try:
        daily_vocabulary = generate_daily_words()

        opened = DailyVocabularyOpen.objects.filter(
            daily_vocabulary=daily_vocabulary,
            user=request.user,
        ).exists()

        return Response({
            "success": True,
            "opened": opened,
        })

    except Exception:
        return Response(
            {
                "success": False,
                "error": "Unable to get today's vocabulary status.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                },
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def today_vocabulary(request):
    try:
        daily_vocabulary = generate_daily_words()

        serializer = DailyVocabularySerializer(
            daily_vocabulary
        )

        return Response({
            "success": True,
            **serializer.data,
        })

    except Exception:
        return Response(
            {
                "success": False,
                "error": "Unable to generate today's vocabulary.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()

    return Response({
        "success": True,
        "message": "Logged out successfully.",
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "success": True,
        "user": {
            "id": request.user.id,
            "username": request.user.username,
        },
    })

@api_view(["POST"])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    email = serializer.validated_data["email"]

    users = User.objects.filter(
        email__iexact=email,
        is_active=True,
    )

    for user in users:
        token = default_token_generator.make_token(user)

        reset_url = (
            "http://localhost:8081/reset-password/"
            f"?uid={user.pk}&token={token}"
        )

        send_mail(
            subject="Reset your 5 Words Per Day password",
            message=f"Use this link to reset your password:\n\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    return Response({
        "success": True,
        "message": (
            "If an account exists with this email, "
            "a reset link will be sent."
        ),
    })

@api_view(["POST"])
def reset_password(request):
    serializer = ResetPasswordSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    uid = serializer.validated_data["uid"]
    token = serializer.validated_data["token"]
    new_password = serializer.validated_data["new_password"]

    try:
        user = User.objects.get(
            pk=uid
        )
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": "Invalid reset link.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not default_token_generator.check_token(
        user,
        token,
    ):
        return Response(
            {
                "success": False,
                "error": "Invalid or expired reset link.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return Response({
        "success": True,
        "message": "Password reset successfully.",
    })