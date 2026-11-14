"""The PEGELONLINE component."""

import logging

from aiopegelonline import PegelOnline
from aiopegelonline.const import CONNECT_ERRORS

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION, DOMAIN
from .coordinator import PegelOnlineConfigEntry, PegelOnlineDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: PegelOnlineConfigEntry) -> None:
    """Set up PEGELONLINE entry."""
    station_uuid = entry.data[CONF_STATION]

    _LOGGER.debug("Setting up station with uuid %s", station_uuid)

    api = PegelOnline(async_get_clientsession(hass))
    try:
        station = await api.async_get_station_details(station_uuid)
    except CONNECT_ERRORS as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="communication_error",
            translation_placeholders={"error": str(err)},
        ) from err

    coordinator = PegelOnlineDataUpdateCoordinator(hass, entry, api, station)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: PegelOnlineConfigEntry
) -> None:
    """Unload PEGELONLINE entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
