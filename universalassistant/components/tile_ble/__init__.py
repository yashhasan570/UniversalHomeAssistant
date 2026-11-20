"""The Tile BLE integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import TileBleConfigEntry, TileBleCoordinator

PLATFORMS = [Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: UniversalAssistant, entry: TileBleConfigEntry) -> None:
    """Set up Tile BLE from a config entry."""
    coordinator = TileBleCoordinator(hass, entry)
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: UniversalAssistant, entry: TileBleConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
