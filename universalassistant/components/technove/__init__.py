"""The TechnoVE integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import TechnoVEConfigEntry, TechnoVEDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.NUMBER, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: UniversalAssistant, entry: TechnoVEConfigEntry) -> None:
    """Set up TechnoVE from a config entry."""
    coordinator = TechnoVEDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: TechnoVEConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
