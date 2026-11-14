"""Errors for the HLK-SW16 component."""

from universalassistant.exceptions import UniversalAssistantError


class SW16Exception(UniversalAssistantError):
    """Base class for HLK-SW16 exceptions."""


class CannotConnect(SW16Exception):
    """Unable to connect to the HLK-SW16."""
