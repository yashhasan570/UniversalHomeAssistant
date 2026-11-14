"""The Garages Amsterdam integration."""

from odp_amsterdam import ODPAmsterdam

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import (
    GaragesAmsterdamConfigEntry,
    GaragesAmsterdamDataUpdateCoordinator,
)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: GaragesAmsterdamConfigEntry
) -> None:
    """Set up Garages Amsterdam from a config entry."""
    client = ODPAmsterdam(session=async_get_clientsession(hass))
    coordinator = GaragesAmsterdamDataUpdateCoordinator(hass, entry, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: GaragesAmsterdamConfigEntry
) -> None:
    """Unload Garages Amsterdam config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
