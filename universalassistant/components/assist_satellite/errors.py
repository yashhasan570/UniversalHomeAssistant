"""Errors for assist satellite."""

from universalassistant.exceptions import UniversalAssistantError


class AssistSatelliteError(UniversalAssistantError):
    """Base class for assist satellite errors."""


class SatelliteBusyError(AssistSatelliteError):
    """Satellite is busy and cannot handle the request."""
