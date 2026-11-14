"""Integration for humidity triggers and conditions."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

DOMAIN = "humidity"
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = []


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the component."""
    return True
