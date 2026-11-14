"""The Frontier Silicon integration."""

import logging

from afsapi import AFSAPI, FSConnectionError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_PIN, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

from .const import CONF_WEBFSAPI_URL

PLATFORMS = [Platform.MEDIA_PLAYER, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)

type FrontierSiliconConfigEntry = ConfigEntry[AFSAPI]


async def async_setup_entry(
    hass: UniversalAssistant, entry: FrontierSiliconConfigEntry
) -> None:
    """Set up Frontier Silicon from a config entry."""

    webfsapi_url = entry.data[CONF_WEBFSAPI_URL]
    pin = entry.data[CONF_PIN]

    afsapi = AFSAPI(webfsapi_url, pin)

    try:
        await afsapi.get_power()
    except FSConnectionError as exception:
        raise ConfigEntryNotReady from exception

    entry.runtime_data = afsapi

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: FrontierSiliconConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
