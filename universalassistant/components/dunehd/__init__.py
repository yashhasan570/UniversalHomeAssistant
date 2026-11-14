"""The Dune HD component."""

from typing import Final

from pdunehd import DuneHDPlayer

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import UniversalAssistant

PLATFORMS: Final[list[Platform]] = [Platform.MEDIA_PLAYER]


type DuneHDConfigEntry = ConfigEntry[DuneHDPlayer]


async def async_setup_entry(hass: UniversalAssistant, entry: DuneHDConfigEntry) -> None:
    """Set up a config entry."""
    entry.runtime_data = DuneHDPlayer(entry.data[CONF_HOST])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: DuneHDConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
