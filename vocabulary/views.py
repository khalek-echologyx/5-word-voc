from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import DailyVocabularySerializer
from .services import generate_daily_words


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
        return Response(
            {
                "success": False,
                "error": "Unable to generate today's vocabulary.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )