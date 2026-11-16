"""The Internet Printing Protocol (IPP) integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import IPPConfigEntry, IPPDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: IPPConfigEntry) -> None:
    """Set up IPP from a config entry."""
    coordinator = IPPDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: IPPConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
