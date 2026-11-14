"""Support for launching a web browser on the host machine."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import setup_services

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


def setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Listen for browse_url events."""
    setup_services(hass)
    return True
