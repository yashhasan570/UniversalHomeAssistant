"""The blackbird component."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import setup_services

CONFIG_SCHEMA = cv.platform_only_config_schema(DOMAIN)


def setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the blackbird component."""
    setup_services(hass)
    return True
