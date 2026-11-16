"""Component providing default configuration for new users."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

DOMAIN = "default_config"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Initialize default configuration."""
    return True
