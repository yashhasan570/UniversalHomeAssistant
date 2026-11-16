"""Provide a mock package component."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

from .const import TEST  # noqa: F401

DOMAIN = "test_package"


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
