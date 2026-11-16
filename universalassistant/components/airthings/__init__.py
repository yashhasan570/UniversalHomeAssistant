"""The Airthings integration."""

from datetime import timedelta
import logging

from airthings import Airthings

from universalassistant.const import CONF_ID, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_SECRET
from .coordinator import AirthingsConfigEntry, AirthingsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(minutes=6)


async def async_setup_entry(hass: UniversalAssistant, entry: AirthingsConfigEntry) -> None:
    """Set up Airthings from a config entry."""
    airthings = Airthings(
        entry.data[CONF_ID],
        entry.data[CONF_SECRET],
        async_get_clientsession(hass),
    )

    coordinator = AirthingsDataUpdateCoordinator(hass, airthings, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AirthingsConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
