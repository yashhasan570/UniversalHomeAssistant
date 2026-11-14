"""The pvpc_hourly_pricing integration to collect Spain official electric prices."""

from universalassistant.const import CONF_API_TOKEN, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .coordinator import ElecPricesDataUpdateCoordinator, PVPCConfigEntry
from .helpers import get_enabled_sensor_keys

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: PVPCConfigEntry) -> None:
    """Set up pvpc hourly pricing from a config entry."""
    entity_registry = er.async_get(hass)
    sensor_keys = get_enabled_sensor_keys(
        using_private_api=entry.data.get(CONF_API_TOKEN) is not None,
        entries=er.async_entries_for_config_entry(entity_registry, entry.entry_id),
    )
    coordinator = ElecPricesDataUpdateCoordinator(hass, entry, sensor_keys)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: PVPCConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
