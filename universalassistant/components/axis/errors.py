"""Errors for the Axis component."""

from universalassistant.exceptions import UniversalAssistantError


class AxisException(UniversalAssistantError):
    """Base class for Axis exceptions."""


class AlreadyConfigured(AxisException):
    """Device is already configured."""


class AuthenticationRequired(AxisException):
    """Unknown error occurred."""


class CannotConnect(AxisException):
    """Unable to connect to the device."""


class UserLevel(AxisException):
    """User level too low."""
