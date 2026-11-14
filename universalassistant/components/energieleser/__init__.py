"""The energieleser integration."""

from energieleser import EnergieleserClient

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import EnergieleserConfigEntry, EnergieleserCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(
    hass: UniversalAssistant, entry: EnergieleserConfigEntry
) -> None:
    """Set up energieleser from a config entry."""
    client = EnergieleserClient(
        host=entry.data[CONF_HOST],
        session=async_get_clientsession(hass),
    )
    coordinator = EnergieleserCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: EnergieleserConfigEntry
) -> None:
    """Unload an energieleser config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
