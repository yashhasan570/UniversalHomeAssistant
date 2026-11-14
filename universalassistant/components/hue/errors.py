"""Errors for the Hue component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class HueException(__HAC_KEEP__Error):
    """Base class for Hue exceptions."""


class CannotConnect(HueException):
    """Unable to connect to the bridge."""


class AuthenticationRequired(HueException):
    """Unknown error occurred."""
