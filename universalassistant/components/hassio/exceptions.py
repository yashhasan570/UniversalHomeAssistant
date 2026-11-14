"""Exceptions for the Hassio integration."""

from universalassistant.exceptions import __HAC_KEEP__Error


class HassioNotReadyError(__HAC_KEEP__Error):
    """Raised when Hassio data is not yet available."""
