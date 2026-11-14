"""The openSenseMap integration."""

from opensensemap_api import OpenSenseMap

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION_ID
from .coordinator import OpenSenseMapConfigEntry, OpenSenseMapCoordinator

PLATFORMS: list[Platform] = [Platform.AIR_QUALITY, Platform.SENSOR]


async def async_setup_entry(
    hass: UniversalAssistant, entry: OpenSenseMapConfigEntry
) -> None:
    """Set up openSenseMap from a config entry."""
    session = async_get_clientsession(hass)
    api = OpenSenseMap(entry.data[CONF_STATION_ID], session)
    coordinator = OpenSenseMapCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: OpenSenseMapConfigEntry
) -> None:
    """Unload an openSenseMap config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
