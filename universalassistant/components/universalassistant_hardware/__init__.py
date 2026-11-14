"""The __HA_KEEP__ Hardware integration."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DATA_COMPONENT, DOMAIN
from .helpers import HardwareInfoDispatcher

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = [
    "DOMAIN",
]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the component."""

    hass.data[DATA_COMPONENT] = HardwareInfoDispatcher(hass)

    return True
