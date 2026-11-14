"""The blackbird component."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import setup_services

CONFIG_SCHEMA = cv.platform_only_config_schema(DOMAIN)


def setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the blackbird component."""
    setup_services(hass)
    return True
