"""The Altruist integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import AltruistConfigEntry, AltruistDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: AltruistConfigEntry) -> None:
    """Set up Altruist from a config entry."""

    coordinator = AltruistDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AltruistConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
