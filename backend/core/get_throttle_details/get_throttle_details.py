import re
from datetime import datetime, timedelta  # type: ignore

import pytz
from django.conf import settings
from rest_framework.throttling import BaseThrottle

from .types import ThrottleRateLimitType


def upper_camel_to_snake_case(string: str) -> str:
    """
    Converts a string from UpperCamelCase to snake_case,
    removing unnecessary suffixes like 'RateThrottle'.
    """
    # Remove 'RateThrottle' from the class name if present
    string = string.replace("RateThrottle", "")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()


def parse_throttle_rate(rate: str) -> tuple[int, int] | None:
    """
    Parse throttle rate string (e.g., '100/day') and return duration in seconds.
    """
    if not rate:
        return None

    match = re.match(r"(\d+)/(second|minute|hour|day)", rate)
    if match:
        num_requests, period = match.groups()
        duration_in_seconds = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
        }.get(period, 0)
        return int(num_requests), duration_in_seconds
    return None


def get_throttle_details(self) -> list[ThrottleRateLimitType]:
    """
    Retrieve throttle details for all specified throttle classes.

    Returns:
        dict[str, ThrottleRateLimitType]: A dictionary mapping throttle class names to their details.
    """
    if not hasattr(self, "throttle_classes"):
        raise AttributeError(
            f"throttle_classes not found on class {type(self).__name__}"
        )

    if not hasattr(self, "request"):
        raise AttributeError(f"request not found on class {type(self).__name__}")

    throttle_details: list[ThrottleRateLimitType] = []

    for throttle_class in self.throttle_classes:
        # Instantiate the throttle class
        throttle: BaseThrottle = throttle_class()

        # Get throttle rate from settings using the class name
        throttle_name = upper_camel_to_snake_case(throttle_class.__name__)

        # Match throttle name to the correct setting in DEFAULT_THROTTLE_RATES
        throttle_rate = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {}).get(
            throttle_name
        )

        if not throttle_rate:
            continue  # Skip this throttle class if no rate is found in settings

        # Parse the throttle rate
        parsed_rate = parse_throttle_rate(throttle_rate)

        if not parsed_rate:
            continue  # Skip this throttle class if the rate is invalid or missing

        limit, duration = parsed_rate

        # Retrieve the cache key
        cache_key = throttle.get_cache_key(self.request, self)  # type: ignore
        if cache_key:
            # Access the backend to count requests made
            history = throttle.cache.get(cache_key, [])  # type: ignore
        else:
            history = []

        # Calculate remaining requests
        remaining = max(0, limit - len(history))

        # Determine reset time
        if history:
            # Convert the first timestamp in the history to a datetime object
            first_request_time = datetime.fromtimestamp(history[0], tz=pytz.UTC)
            reset_time = first_request_time + timedelta(seconds=duration)
        else:
            reset_time = datetime.now(pytz.UTC) + timedelta(seconds=duration)

        # Calculate retry after in seconds
        retry_after = max(0, int((reset_time - datetime.now(pytz.UTC)).total_seconds()))

        # Add throttle details to the dictionary
        throttle_details.append(
            {
                "type": throttle_name,
                "limit": limit,
                "remaining": remaining,
                "reset_time": reset_time.isoformat(),
                "retry_after": f"{retry_after} seconds",
            }
        )

    return throttle_details
