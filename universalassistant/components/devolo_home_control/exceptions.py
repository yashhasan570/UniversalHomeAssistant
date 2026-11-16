"""Custom exceptions for the devolo_home_control integration."""

from universalassistant.exceptions import UniversalAssistantError


class CredentialsInvalid(UniversalAssistantError):
    """Given credentials are invalid."""


class UuidChanged(UniversalAssistantError):
    """UUID of the user changed."""
