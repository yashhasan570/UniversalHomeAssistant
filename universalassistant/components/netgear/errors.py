"""Errors for the Netgear component."""

from universalassistant.exceptions import UniversalAssistantError


class NetgearException(UniversalAssistantError):
    """Base class for Netgear exceptions."""


class CannotLoginException(NetgearException):
    """Unable to login to the router."""
