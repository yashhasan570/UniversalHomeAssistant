"""The Fing integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError

from .coordinator import FingConfigEntry, FingDataUpdateCoordinator

PLATFORMS = [Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: UniversalAssistant, config_entry: FingConfigEntry) -> None:
    """Set up the Fing component."""

    coordinator = FingDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.data.network_id is None:
        raise ConfigEntryError(
            "The Agent's API version is outdated."
            " Please update the agent to the latest version."
        )

    config_entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, config_entry: FingConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(config_entry, PLATFORMS)
