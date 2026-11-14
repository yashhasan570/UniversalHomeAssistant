"""Errors for the Acmeda Pulse component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class PulseException(__HAC_KEEP__Error):
    """Base class for Acmeda Pulse exceptions."""


class CannotConnect(PulseException):
    """Unable to connect to the bridge."""
