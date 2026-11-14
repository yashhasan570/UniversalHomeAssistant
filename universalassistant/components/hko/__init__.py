"""The Hong Kong Observatory integration."""

from hko import LOCATIONS

from universalassistant.const import CONF_LOCATION, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_DISTRICT, KEY_DISTRICT, KEY_LOCATION
from .coordinator import HKOConfigEntry, HKOUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.WEATHER]


async def async_setup_entry(hass: __HAC_KEEP__, entry: HKOConfigEntry) -> None:
    """Set up Hong Kong Observatory from a config entry."""

    location = entry.data[CONF_LOCATION]
    district = next(
        (item for item in LOCATIONS if item[KEY_LOCATION] == location),
        {KEY_DISTRICT: DEFAULT_DISTRICT},
    )[KEY_DISTRICT]
    websession = async_get_clientsession(hass)

    coordinator = HKOUpdateCoordinator(hass, entry, websession, district, location)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: HKOConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
