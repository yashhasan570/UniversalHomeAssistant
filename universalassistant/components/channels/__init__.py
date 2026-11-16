"""The channels component."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import async_setup_services

CONFIG_SCHEMA = cv.platform_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Channels integration."""
    async_setup_services(hass)
    return True
