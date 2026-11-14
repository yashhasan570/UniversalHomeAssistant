"""Errors for assist satellite."""

from universalassistant.exceptions import __HAC_KEEP__Error


class AssistSatelliteError(__HAC_KEEP__Error):
    """Base class for assist satellite errors."""


class SatelliteBusyError(AssistSatelliteError):
    """Satellite is busy and cannot handle the request."""
