"""The Sky Remote Control integration."""

import logging

from skyboxremote import RemoteControl, SkyBoxConnectionError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_PORT, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

PLATFORMS = [Platform.REMOTE]

_LOGGER = logging.getLogger(__name__)


type SkyRemoteConfigEntry = ConfigEntry[RemoteControl]


async def async_setup_entry(hass: UniversalAssistant, entry: SkyRemoteConfigEntry) -> None:
    """Set up Sky remote."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]

    _LOGGER.debug("Setting up Host: %s, Port: %s", host, port)
    remote = RemoteControl(host, port)
    try:
        await remote.check_connectable()
    except SkyBoxConnectionError as e:
        raise ConfigEntryNotReady from e

    entry.runtime_data = remote
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: SkyRemoteConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
