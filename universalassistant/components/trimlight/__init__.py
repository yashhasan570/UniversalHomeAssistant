"""The Trimlight integration."""

from aiotrimlight import TrimlightClient

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import TrimlightConfigEntry, TrimlightCoordinator

PLATFORMS = (Platform.LIGHT,)


async def async_setup_entry(hass: UniversalAssistant, entry: TrimlightConfigEntry) -> None:
    """Set up Trimlight from a config entry."""
    client = TrimlightClient(
        entry.data[CONF_HOST],
        async_get_clientsession(hass),
    )

    coordinator = TrimlightCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: TrimlightConfigEntry) -> None:
    """Unload a Trimlight config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
