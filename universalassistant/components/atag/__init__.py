"""The ATAG Integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import AtagConfigEntry, AtagDataUpdateCoordinator

DOMAIN = "atag"
PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.WATER_HEATER]


async def async_setup_entry(hass: __HAC_KEEP__, entry: AtagConfigEntry) -> None:
    """Set up Atag integration from a config entry."""

    coordinator = AtagDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    if entry.unique_id is None:
        hass.config_entries.async_update_entry(entry, unique_id=coordinator.atag.id)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: AtagConfigEntry) -> None:
    """Unload Atag config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
