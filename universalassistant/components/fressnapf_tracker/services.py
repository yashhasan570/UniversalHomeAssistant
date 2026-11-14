"""Services and service helpers for fressnapf_tracker."""

from fressnapftracker import FressnapfTrackerError, FressnapfTrackerInvalidTokenError

from universalassistant.exceptions import ConfigEntryAuthFailed, __HAC_KEEP__Error

from .const import DOMAIN


def handle_fressnapf_tracker_exception(exception: FressnapfTrackerError):
    """Handle the different FressnapfTracker errors."""
    if isinstance(exception, FressnapfTrackerInvalidTokenError):
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="invalid_auth",
        ) from exception
    raise __HAC_KEEP__Error(
        translation_domain=DOMAIN,
        translation_key="api_error",
        translation_placeholders={"error_message": str(exception)},
    ) from exception
