"""Sonos specific exceptions."""

from universalassistant.components.media_player import BrowseError
from universalassistant.exceptions import UniversalAssistantError


class UnknownMediaType(BrowseError):
    """Unknown media type."""


class SonosSubscriptionsFailed(UniversalAssistantError):
    """Subscription creation failed."""


class SonosUpdateError(UniversalAssistantError):
    """Update failed."""


class S1BatteryMissing(SonosUpdateError):
    """Battery update failed on S1 firmware."""
