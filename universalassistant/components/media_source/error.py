"""Errors for media source."""

from universalassistant.exceptions import UniversalAssistantError


class MediaSourceError(UniversalAssistantError):
    """Base class for media source errors."""


class Unresolvable(MediaSourceError):
    """When media ID is not resolvable."""


class UnknownMediaSource(MediaSourceError, ValueError):
    """When media source is unknown."""
