"""Exceptions for the Hassio integration."""

from universalassistant.exceptions import UniversalAssistantError


class HassioNotReadyError(UniversalAssistantError):
    """Raised when Hassio data is not yet available."""
