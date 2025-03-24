import logging
from typing import Literal

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsOwner(BasePermission):
    """Custom permission class that checks if the user
    is the owner of the requested object.
    """

    def has_object_permission(self, request, view, obj) -> Literal[True]:
        """Check if the authenticated user is the owner of the object."""

        # Handle unauthenticated users
        if not request.user or not request.user.is_authenticated:
            logger.warning(
                f"Unauthenticated access attempt to {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')}."
            )
            raise PermissionDenied(
                {
                    "message": "Authentication failed - valid credentials required",
                    "errors": {
                        "detail": "Access denied. Please provide valid authentication credentials in the Authorization header.",
                        "code": "authentication_required",
                    },
                }
            )

        # Check if the user is the owner of the object
        if hasattr(obj, "owner") and obj.owner == request.user:
            logger.info(
                f"User {request.user.username or request.user.email} authorized "
                f"as the owner of object ID {getattr(obj, 'id', 'unknown')}."
            )
            return True

        # Log and raise a permission denied error for non-owners
        logger.warning(
            f"User {request.user.username or request.user.email} is not the owner of object ID {getattr(obj, 'id', 'unknown')}."
        )
        raise PermissionDenied(
            {
                "message": "Access denied - insufficient privileges",
                "errors": {
                    "detail": "You do not have sufficient permissions to perform this action. Only the resource owner can access this endpoint.",
                    "code": "not_owner",
                    "required_role": "owner",
                    "current_user": request.user.username or request.user.email,
                    "object_id": getattr(obj, "id", "unknown"),
                },
            }
        )
