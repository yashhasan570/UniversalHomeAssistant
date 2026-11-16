"""The Essent integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import EssentConfigEntry, EssentDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: EssentConfigEntry) -> None:
    """Set up Essent from a config entry."""
    coordinator = EssentDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Start listener updates on the hour to advance cached tariffs
    coordinator.start_listener_schedule()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: EssentConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
