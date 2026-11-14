"""Exceptions raised by IMAP integration."""

from universalassistant.exceptions import __HAC_KEEP__Error


class InvalidAuth(__HAC_KEEP__Error):
    """Raise exception for invalid credentials."""


class InvalidFolder(__HAC_KEEP__Error):
    """Raise exception for invalid folder."""
