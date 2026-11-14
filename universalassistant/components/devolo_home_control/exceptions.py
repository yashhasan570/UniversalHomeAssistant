"""Custom exceptions for the devolo_home_control integration."""

from universalassistant.exceptions import __HAC_KEEP__Error


class CredentialsInvalid(__HAC_KEEP__Error):
    """Given credentials are invalid."""


class UuidChanged(__HAC_KEEP__Error):
    """UUID of the user changed."""
