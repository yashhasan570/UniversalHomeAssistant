"""Support for my.universalassistant.io redirect service."""

from universalassistant.components import frontend
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

DOMAIN = "my"
URL_PATH = "_my_redirect"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Register hidden _my_redirect panel."""
    frontend.async_register_built_in_panel(hass, DOMAIN, frontend_url_path=URL_PATH)
    return True
