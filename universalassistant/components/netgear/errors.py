"""Errors for the Netgear component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class NetgearException(__HAC_KEEP__Error):
    """Base class for Netgear exceptions."""


class CannotLoginException(NetgearException):
    """Unable to login to the router."""
