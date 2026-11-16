"""Errors for the Media Player component."""

from universalassistant.exceptions import UniversalAssistantError


class MediaPlayerException(UniversalAssistantError):
    """Base class for Media Player exceptions."""


class BrowseError(MediaPlayerException):
    """Error while browsing."""


class SearchError(MediaPlayerException):
    """Error while searching."""
