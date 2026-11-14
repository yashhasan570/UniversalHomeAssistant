"""Xthings Cloud integration for Universal Universal Home Assistant."""

from ha_xthings_cloud import XthingsCloudApiClient

from universalassistant.const import CONF_TOKEN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import PLATFORMS
from .coordinator import XthingsCloudConfigEntry, XthingsCloudCoordinator


async def async_setup_entry(
    hass: UniversalAssistant, entry: XthingsCloudConfigEntry
) -> None:
    """Set up config entry."""
    session = async_get_clientsession(hass)
    client = XthingsCloudApiClient(session, token=entry.data[CONF_TOKEN])

    coordinator = XthingsCloudCoordinator(hass, client, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await coordinator.async_start_websocket()


async def async_unload_entry(
    hass: UniversalAssistant, entry: XthingsCloudConfigEntry
) -> None:
    """Unload config entry."""
    coordinator = entry.runtime_data
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    await coordinator.async_stop_websocket()
