import logging

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class IsAuthenticated(permissions.IsAuthenticated):
    """Custom authentication permission class that extends DRF's IsAuthenticated."""

    def has_permission(self, request, view) -> bool:
        """Check if the request has valid authentication and log details."""

        if request.user.is_superuser:
            # Allow superusers to bypass further authentication checks
            logger.info(
                f"Superuser {request.user.username or request.user.email} authenticated successfully "
                f"for {request.method} {request.path}."
            )
            return True

        if not request.user or not request.user.is_authenticated:
            # Log and raise custom permission denied exception for unauthenticated users
            logger.warning(
                f"Unauthenticated access attempt to {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')}."
            )
            raise PermissionDenied(
                {
                    "message": "Authentication failed - Access denied",
                    "errors": {
                        "detail": "Authentication credentials were not provided or are invalid. Please include a valid authentication token in the Authorization header.",
                    },
                }
            )

        # Log successful authentication
        logger.info(
            f"Authenticated user {request.user.username or request.user.email} successfully accessed "
            f"{request.method} {request.path}."
        )
        return True
