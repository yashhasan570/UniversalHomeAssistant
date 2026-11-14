"""Errors for the HLK-SW16 component."""

from universalassistant.exceptions import __HAC_KEEP__Error


class SW16Exception(__HAC_KEEP__Error):
    """Base class for HLK-SW16 exceptions."""


class CannotConnect(SW16Exception):
    """Unable to connect to the HLK-SW16."""
