"""The MJPEG IP Camera integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .camera import MjpegCamera
from .const import CONF_MJPEG_URL, CONF_STILL_IMAGE_URL, DOMAIN, PLATFORMS
from .util import filter_urllib3_logging

__all__ = [
    "CONF_MJPEG_URL",
    "CONF_STILL_IMAGE_URL",
    "MjpegCamera",
    "filter_urllib3_logging",
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the MJPEG IP Camera integration."""
    filter_urllib3_logging()
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_reload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when it changed."""
    await hass.config_entries.async_reload(entry.entry_id)
