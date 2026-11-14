"""The errors of Epson integration."""

from universalassistant import exceptions


class CannotConnect(exceptions.UniversalAssistantError):
    """Error to indicate we cannot connect."""


class PoweredOff(exceptions.UniversalAssistantError):
    """Error to indicate projector is off."""
