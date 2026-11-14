"""Provide a mock standalone component."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

DOMAIN = "test_standalone"


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
