"""Errors for the Media Player component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class MediaPlayerException(__HAC_KEEP__Error):
    """Base class for Media Player exceptions."""


class BrowseError(MediaPlayerException):
    """Error while browsing."""


class SearchError(MediaPlayerException):
    """Error while searching."""
