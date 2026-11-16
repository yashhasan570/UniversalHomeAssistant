"""The buienradar integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .util import BrData

PLATFORMS = [Platform.CAMERA, Platform.SENSOR, Platform.WEATHER]

type BuienRadarConfigEntry = ConfigEntry[dict[Platform, BrData]]


async def async_setup_entry(hass: UniversalAssistant, entry: BuienRadarConfigEntry) -> None:
    """Set up buienradar from a config entry."""
    entry.runtime_data = {}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_update_options))


async def async_unload_entry(hass: UniversalAssistant, entry: BuienRadarConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    for platform in PLATFORMS:
        if (data := entry.runtime_data.get(platform)) and (
            unsub := data.unsub_schedule_update
        ):
            unsub()


async def async_update_options(
    hass: UniversalAssistant, config_entry: BuienRadarConfigEntry
) -> None:
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)
