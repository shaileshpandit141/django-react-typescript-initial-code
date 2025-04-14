import logging
from typing import Any

from core.response import Response

logger = logging.getLogger(__name__)


def create_error_response(
    message: str, errors: Any, status: int | None = None
) -> Response:
    """Helper function to create error response"""
    error_details: dict[str, Any] = {
        "detail": "Something went wrong. Please try again later or contact support if the issue persists."
    }

    try:
        errors_tuple = getattr(errors, "args", tuple())
        if len(errors_tuple) > 0 and isinstance(errors_tuple[0], dict):
            error_details = errors_tuple[0]
        elif hasattr(errors, "detail"):
            error_details["detail"] = errors.detail
        elif hasattr(errors, "message"):
            error_details["detail"] = errors.message
        elif isinstance(errors, dict):
            error_details = errors
        elif isinstance(errors, str):
            error_details["detail"] = errors
        else:
            error_details["detail"] = str(errors)
    except Exception as error:
        logger.error(
            f"An unexpected error occurred while processing error details: {str(error)}"
        )
        error_details["detail"] = (
            "An unexpected error occurred. Our team has been notified."
        )

    return Response(
        {
            "message": message or "Error occurred",
            "data": {},
            "errors": error_details,
        },
        status,
    )
