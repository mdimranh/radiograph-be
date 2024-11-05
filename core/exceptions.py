from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import ReturnDict


class Unauthorized(APIException):
    status_code = 403
    default_detail = "You are not allowed to use this profile"
    default_code = "forbidden"

    def __init__(self, detail=None, code=None):
        if isinstance(detail, dict):
            # Make sure the detail is serialized as a dict properly
            self.detail = ReturnDict(detail, serializer=None)
        else:
            self.detail = {"message": detail or self.default_detail}
        if code:
            self.detail["code"] = code
        else:
            self.detail["code"] = self.default_code


def custom_exception_handler(exc, context):
    from rest_framework.views import exception_handler

    # Call the default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        # Handle exceptions that are not caught by DRF's default exception handler
        if isinstance(exc, Http404):
            response = Response(
                {
                    "error": True,
                    "message": "Not found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        elif isinstance(exc, Unauthorized):
            response = Response(
                {
                    "error": True,
                    "message": "Unauthorized",
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            response.remove_cookie("access-token")
            response.remove_cookie("refresh-token")
        elif isinstance(exc, PermissionDenied):
            response = Response(
                {
                    "error": True,
                    "message": "Permission denied",
                    "status_code": status.HTTP_403_FORBIDDEN,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif isinstance(exc, APIException):
            response = Response(
                {"error": True, "message": str(exc), "status_code": exc.status_code},
                status=exc.status_code,
            )
        else:
            # General error fallback
            response = Response(
                {
                    "error": True,
                    "message": "Internal server error",
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return response
