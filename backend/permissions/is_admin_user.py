import logging

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class IsAdminUser(permissions.IsAdminUser):
    """Custom authentication permission class that extends DRF's IsAdminUser."""

    def has_permission(self, request, view) -> bool:
        """Check if the request has valid authentication and staff privileges."""

        if request.user.is_superuser:
            # Allow superusers to bypass further authentication checks
            logger.info(
                f"Superuser {request.user.username or request.user.email} "
                f"authenticated successfully for {request.method} {request.path}."
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
                    "message": "Authentication required on this endpoint",
                    "errors": {
                        "deatil": "You must include a valid authentication token in the Authorization header."
                    },
                }
            )

        if not request.user.is_staff:
            # Log and raise custom permission denied exception for non-staff users
            logger.warning(
                f"Non-staff user {request.user.username or request.user.email} attempted to access "
                f"{request.method} {request.path} from {request.META.get('REMOTE_ADDR')}."
            )
            raise PermissionDenied(
                {
                    "message": "Staff access required on this endpoint",
                    "errors": {"detail": "This endpoint requires staff privileges."},
                }
            )

        # Log successful staff authentication
        logger.info(
            f"Staff user {request.user.username or request.user.email} authenticated successfully "
            f"for {request.method} {request.path}."
        )
        return True
