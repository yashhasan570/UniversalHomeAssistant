"""Errors for the Mikrotik component."""

from universalassistant.exceptions import UniversalAssistantError


class CannotConnect(UniversalAssistantError):
    """Unable to connect to the hub."""


class LoginError(UniversalAssistantError):
    """Component got logged out."""
