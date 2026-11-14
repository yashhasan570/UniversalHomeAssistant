"""The Universal Universal Home Assistant Hardware integration."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DATA_COMPONENT, DOMAIN
from .helpers import HardwareInfoDispatcher

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = [
    "DOMAIN",
]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the component."""

    hass.data[DATA_COMPONENT] = HardwareInfoDispatcher(hass)

    return True
