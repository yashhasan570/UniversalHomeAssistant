"""Sonos specific exceptions."""

from universalassistant.components.media_player import BrowseError
from universalassistant.exceptions import __HAC_KEEP__Error


class UnknownMediaType(BrowseError):
    """Unknown media type."""


class SonosSubscriptionsFailed(__HAC_KEEP__Error):
    """Subscription creation failed."""


class SonosUpdateError(__HAC_KEEP__Error):
    """Update failed."""


class S1BatteryMissing(SonosUpdateError):
    """Battery update failed on S1 firmware."""
