"""Support for Fumis pellet stoves."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import FumisConfigEntry, FumisDataUpdateCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: UniversalAssistant, entry: FumisConfigEntry) -> None:
    """Set up Fumis from a config entry."""
    coordinator = FumisDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: FumisConfigEntry) -> None:
    """Unload Fumis config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
