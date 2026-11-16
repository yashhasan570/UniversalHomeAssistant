"""The Pure Energie integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

from .coordinator import PureEnergieConfigEntry, PureEnergieDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: PureEnergieConfigEntry) -> None:
    """Set up Pure Energie from a config entry."""

    coordinator = PureEnergieDataUpdateCoordinator(hass, entry)
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await coordinator.gridnet.close()
        raise

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: PureEnergieConfigEntry
) -> None:
    """Unload Pure Energie config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
