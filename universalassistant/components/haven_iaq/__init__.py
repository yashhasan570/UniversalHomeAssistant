"""HAVEN IAQ local API integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import HavenConfigEntry, HavenDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: HavenConfigEntry) -> None:
    """Set up HAVEN IAQ from a config entry."""
    coordinator = HavenDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: HavenConfigEntry) -> None:
    """Unload a HAVEN IAQ config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
