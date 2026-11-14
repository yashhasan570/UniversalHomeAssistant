"""Component with embedded platforms."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

DOMAIN = "test_embedded"


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Mock config."""
    return True
