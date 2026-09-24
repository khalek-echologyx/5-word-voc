from rest_framework.response import Response
from rest_framework import status


def api_error_response(message):
    return Response(
        {
            "success": False,
            "error": message,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )