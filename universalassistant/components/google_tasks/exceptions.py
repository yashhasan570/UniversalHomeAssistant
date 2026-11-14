"""Exceptions for Google Tasks api calls."""

from universalassistant.exceptions import UniversalAssistantError


class GoogleTasksApiError(UniversalAssistantError):
    """Error talking to the Google Tasks API."""
