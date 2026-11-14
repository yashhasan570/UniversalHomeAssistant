"""Errors for the Mikrotik component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class CannotConnect(__HAC_KEEP__Error):
    """Unable to connect to the hub."""


class LoginError(__HAC_KEEP__Error):
    """Component got logged out."""
