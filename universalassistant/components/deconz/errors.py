"""Errors for the deCONZ component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class DeconzException(__HAC_KEEP__Error):
    """Base class for deCONZ exceptions."""


class AlreadyConfigured(DeconzException):
    """Gateway is already configured."""


class AuthenticationRequired(DeconzException):
    """Unknown error occurred."""


class CannotConnect(DeconzException):
    """Unable to connect to the gateway."""
