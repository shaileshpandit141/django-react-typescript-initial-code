# Types imports
from typing import NoReturn

# Django REST framework imports
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView

# Local imports
from quick_utils.response import Response
from quick_utils.get_throttle_details import get_throttle_details
from permissions import AllowAny
from throttling import AnonRateThrottle


class SigninTokenRefreshAPIView(TokenRefreshView):
    """Custom token refresh view for handling JWT token refresh operations."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs) -> NoReturn:
        """Customize serializer to handle refresh token field name."""

        data = self.request.data.copy()  # type: ignore
        refresh_token = data.pop('refresh_token', None)
        if refresh_token and isinstance(refresh_token, list):
            if len(refresh_token) > 0:
                refresh_token = refresh_token[0]

        if not refresh_token:
            raise serializers.ValidationError({
                'refresh_token': 'This field is required.'
            })

        data['refresh'] = refresh_token
        return super().get_serializer(data=data)

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({
                    "status": "succeeded",
                    "message": "Token refreshed successfully",
                    "data": {
                        "access_token": response.data.get("access", None)  # type: ignore
                    },
                    "errors": None,
                    "meta": {
                        "rate_limit": get_throttle_details(self)
                    }
                }, status.HTTP_200_OK)

            # Invalid or expired refresh token
            return Response({
                "status": "failed",
                'message': 'Failed to refresh token',
                "data": None,
                'errors': [{
                    "field": "refresh_token",
                    "code": "invalid_refresh_token",
                    "message": "Invalid or expired refresh token",
                    "details": None
                }],
                "meta": {
                    "rate_limit": get_throttle_details(self)
                }
            }, status.HTTP_400_BAD_REQUEST)

        except ValidationError as error:
            # Handle case where no refresh token is provided
            if 'refresh_token' in str(error):
                return Response({
                    "status": "failed",
                    'message': 'Refresh token is required',
                    "data": None,
                    'errors': [{
                        "field": "refresh_token",
                        "code": "invalid_refresh_token",
                        "message": "This field is required.",
                        "details": None
                    }],
                    "meta": {
                        "rate_limit": get_throttle_details(self)
                    }
                }, status.HTTP_400_BAD_REQUEST)

            # Catch other validation errors
            return Response({
                "status": "failed",
                'message': 'Invalid refresh token provided',
                "data": None,
                'errors': [{
                    "field": "refresh_token",
                    "code": "invalid_refresh_token",
                    "message": "The refresh token provided is invalid or expired.",
                    "details": None
                }],
                "meta": {
                    "rate_limit": get_throttle_details(self)
                }
            }, status.HTTP_400_BAD_REQUEST)
