"""The brunt component."""

from universalassistant.core import UniversalAssistant

from .const import PLATFORMS
from .coordinator import BruntConfigEntry, BruntCoordinator


async def async_setup_entry(hass: UniversalAssistant, entry: BruntConfigEntry) -> None:
    """Set up Brunt using config flow."""
    coordinator = BruntCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: BruntConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
