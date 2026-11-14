"""Errors for the Plex integration."""

from universalassistant.exceptions import UniversalAssistantError


class PlexException(UniversalAssistantError):
    """Base class for Plex exceptions."""


class NoServersFound(PlexException):
    """No servers found on Plex account."""


class ServerNotSpecified(PlexException):
    """Multiple servers linked to account without choice provided."""


class ShouldUpdateConfigEntry(PlexException):
    """Config entry data is out of date and should be updated."""


class MediaNotFound(PlexException):
    """Requested media was not found."""
