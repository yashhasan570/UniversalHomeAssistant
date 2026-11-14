"""Exceptions raised by IMAP integration."""

from universalassistant.exceptions import UniversalAssistantError


class InvalidAuth(UniversalAssistantError):
    """Raise exception for invalid credentials."""


class InvalidFolder(UniversalAssistantError):
    """Raise exception for invalid folder."""
