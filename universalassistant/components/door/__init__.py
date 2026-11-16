"""Integration for door triggers."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

DOMAIN = "door"
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the component."""
    return True
