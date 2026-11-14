"""The html5 component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, REGISTRATIONS_FILE
from .http import async_register_http_views
from .notify import _load_config
from .services import async_setup_services
from .websocket_api import async_register_websocket_api

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS = [Platform.EVENT, Platform.NOTIFY]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the HTML5 services."""

    async_setup_services(hass)
    async_register_websocket_api(hass)

    json_path = hass.config.path(REGISTRATIONS_FILE)
    registrations = await hass.async_add_executor_job(_load_config, json_path)

    async_register_http_views(hass, json_path, registrations)

    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up HTML5 from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
