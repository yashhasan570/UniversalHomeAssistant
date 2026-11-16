"""The CO2 Signal integration."""

from aioelectricitymaps import ElectricityMaps

from universalassistant.const import CONF_API_KEY, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import CO2SignalConfigEntry, CO2SignalCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: CO2SignalConfigEntry) -> None:
    """Set up CO2 Signal from a config entry."""
    session = async_get_clientsession(hass)
    coordinator = CO2SignalCoordinator(
        hass, entry, ElectricityMaps(token=entry.data[CONF_API_KEY], session=session)
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: CO2SignalConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
