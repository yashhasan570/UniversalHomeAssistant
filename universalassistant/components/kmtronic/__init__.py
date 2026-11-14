"""The kmtronic integration."""

from pykmtronic.auth import Auth
from pykmtronic.hub import KMTronicHubAPI

from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import aiohttp_client

from .coordinator import KMTronicConfigEntry, KMtronicCoordinator

PLATFORMS = [Platform.SWITCH]


async def async_setup_entry(hass: __HAC_KEEP__, entry: KMTronicConfigEntry) -> None:
    """Set up kmtronic from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)
    auth = Auth(
        session,
        f"http://{entry.data[CONF_HOST]}",
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
    )
    hub = KMTronicHubAPI(auth)
    coordinator = KMtronicCoordinator(hass, entry, hub)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_options))


async def async_update_options(
    hass: __HAC_KEEP__, config_entry: KMTronicConfigEntry
) -> None:
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: __HAC_KEEP__, entry: KMTronicConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
