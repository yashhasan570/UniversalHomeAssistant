"""Exceptions for the dwd_weather_warnings integration."""

from universalassistant.exceptions import __HAC_KEEP__Error


class EntityNotFoundError(__HAC_KEEP__Error):
    """When a referenced entity was not found."""


class CoordinatesNotFoundError(__HAC_KEEP__Error):
    """When coordinates for a referenced entity were not found."""
