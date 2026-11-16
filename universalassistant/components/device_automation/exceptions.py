"""Device automation exceptions."""

from universalassistant.exceptions import UniversalAssistantError


class InvalidDeviceAutomationConfig(UniversalAssistantError):
    """When device automation config is invalid."""


class DeviceNotFound(UniversalAssistantError):
    """When referenced device not found."""


class EntityNotFound(UniversalAssistantError):
    """When referenced entity not found."""
