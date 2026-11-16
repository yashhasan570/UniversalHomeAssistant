"""The Volumio integration."""

from dataclasses import dataclass
from typing import Any

from pyvolumio import CannotConnectError, Volumio

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_PORT, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

PLATFORMS = [Platform.MEDIA_PLAYER]


@dataclass
class VolumioData:
    """Volumio data class."""

    volumio: Volumio
    info: dict[str, Any]


type VolumioConfigEntry = ConfigEntry[VolumioData]


async def async_setup_entry(hass: UniversalAssistant, entry: VolumioConfigEntry) -> None:
    """Set up Volumio from a config entry."""

    volumio = Volumio(
        entry.data[CONF_HOST], entry.data[CONF_PORT], async_get_clientsession(hass)
    )
    try:
        info = await volumio.get_system_version()
    except CannotConnectError as error:
        raise ConfigEntryNotReady from error

    entry.runtime_data = VolumioData(volumio=volumio, info=info)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: VolumioConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
