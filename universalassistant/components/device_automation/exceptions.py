"""Device automation exceptions."""

from universalassistant.exceptions import __HAC_KEEP__Error


class InvalidDeviceAutomationConfig(__HAC_KEEP__Error):
    """When device automation config is invalid."""


class DeviceNotFound(__HAC_KEEP__Error):
    """When referenced device not found."""


class EntityNotFound(__HAC_KEEP__Error):
    """When referenced entity not found."""
