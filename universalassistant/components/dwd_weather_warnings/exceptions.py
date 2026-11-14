"""Exceptions for the dwd_weather_warnings integration."""

from universalassistant.exceptions import UniversalAssistantError


class EntityNotFoundError(UniversalAssistantError):
    """When a referenced entity was not found."""


class CoordinatesNotFoundError(UniversalAssistantError):
    """When coordinates for a referenced entity were not found."""
