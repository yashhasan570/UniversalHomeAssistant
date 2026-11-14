"""The errors of Epson integration."""

from universalassistant import exceptions


class CannotConnect(exceptions.__HAC_KEEP__Error):
    """Error to indicate we cannot connect."""


class PoweredOff(exceptions.__HAC_KEEP__Error):
    """Error to indicate projector is off."""
