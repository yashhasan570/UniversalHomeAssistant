"""Provide a mock standalone component."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import ConfigType

DOMAIN = "test_standalone"


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
