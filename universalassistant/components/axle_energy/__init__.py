"""The Axle Energy integration."""

from aioaxlevpp import AxleClient

from universalassistant.const import CONF_API_KEY
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import PLATFORMS
from .coordinator import AxleConfigEntry, AxleCoordinator


async def async_setup_entry(hass: UniversalAssistant, entry: AxleConfigEntry) -> None:
    """Set up Axle Energy from a config entry."""
    coordinator = AxleCoordinator(
        hass, entry, AxleClient(async_get_clientsession(hass), entry.data[CONF_API_KEY])
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AxleConfigEntry) -> None:
    """Unload Axle Energy."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
