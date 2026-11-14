"""Errors for the Hue component."""

from universalassistant.exceptions import UniversalAssistantError


class HueException(UniversalAssistantError):
    """Base class for Hue exceptions."""


class CannotConnect(HueException):
    """Unable to connect to the bridge."""


class AuthenticationRequired(HueException):
    """Unknown error occurred."""
