"""The Adax integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .const import CONNECTION_TYPE, LOCAL
from .coordinator import AdaxCloudCoordinator, AdaxConfigEntry, AdaxLocalCoordinator

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: AdaxConfigEntry) -> None:
    """Set up Adax from a config entry."""
    if entry.data.get(CONNECTION_TYPE) == LOCAL:
        local_coordinator = AdaxLocalCoordinator(hass, entry)
        entry.runtime_data = local_coordinator
    else:
        cloud_coordinator = AdaxCloudCoordinator(hass, entry)
        entry.runtime_data = cloud_coordinator

    await entry.runtime_data.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: AdaxConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_migrate_entry(
    hass: __HAC_KEEP__, config_entry: AdaxConfigEntry
) -> None:
    """Migrate old entry."""
    # convert title and unique_id to string
    if config_entry.version == 1:
        if isinstance(config_entry.unique_id, int):
            hass.config_entries.async_update_entry(  # type: ignore[unreachable]
                config_entry,
                unique_id=str(config_entry.unique_id),
                title=str(config_entry.title),
            )
