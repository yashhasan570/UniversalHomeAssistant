"""Component with embedded platforms."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import ConfigType

DOMAIN = "test_embedded"


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Mock config."""
    return True
