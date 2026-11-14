"""The Harman Luxury Audio integration."""

from aioharmanluxury import HarmanLuxuryClient

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import HarmanLuxuryConfigEntry, HarmanLuxuryCoordinator

_PLATFORMS: list[Platform] = [Platform.MEDIA_PLAYER]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: HarmanLuxuryConfigEntry
) -> None:
    """Set up Harman Luxury from a config entry."""
    client = HarmanLuxuryClient(entry.data[CONF_HOST], async_get_clientsession(hass))
    coordinator = HarmanLuxuryCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: HarmanLuxuryConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, _PLATFORMS)
