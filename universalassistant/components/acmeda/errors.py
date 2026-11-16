"""Errors for the Acmeda Pulse component."""

from universalassistant.exceptions import UniversalAssistantError


class PulseException(UniversalAssistantError):
    """Base class for Acmeda Pulse exceptions."""


class CannotConnect(PulseException):
    """Unable to connect to the bridge."""
