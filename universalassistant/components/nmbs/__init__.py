"""The NMBS component."""

from pyrail import IRail, PyRailError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, NMBS_STATION_DATA

PLATFORMS = [Platform.SENSOR]


CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up NMBS from a config entry."""

    # The station list is shared by all entries, so fetch and cache it only
    # once. Raise ConfigEntryNotReady if the API is unavailable so setup is
    # retried instead of failing permanently.
    if not hass.data.get(NMBS_STATION_DATA):
        api_client = IRail(session=async_get_clientsession(hass))
        message = "Unable to fetch the NMBS station list from the iRail API"
        try:
            station_response = await api_client.get_stations()
        except PyRailError as err:
            raise ConfigEntryNotReady(message) from err
        if station_response is None:
            raise ConfigEntryNotReady(message)
        hass.data[NMBS_STATION_DATA] = station_response.stations

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
