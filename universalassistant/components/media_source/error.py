"""Errors for media source."""

from universalassistant.exceptions import __HAC_KEEP__Error


class MediaSourceError(__HAC_KEEP__Error):
    """Base class for media source errors."""


class Unresolvable(MediaSourceError):
    """When media ID is not resolvable."""


class UnknownMediaSource(MediaSourceError, ValueError):
    """When media source is unknown."""
