"""The Ridder HortiMaX Pro (HortOS) integration."""

from aiohortos import HortosClient

from universalassistant.const import CONF_API_KEY, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import HortimaxConfigEntry, HortimaxCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: HortimaxConfigEntry) -> None:
    """Set up Ridder HortiMaX Pro from a config entry."""
    client = HortosClient(
        entry.data[CONF_API_KEY], session=async_get_clientsession(hass)
    )
    coordinator = HortimaxCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: HortimaxConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
