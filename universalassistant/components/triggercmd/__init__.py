"""The TRIGGERcmd component."""

from triggercmd import client, ha

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_TOKEN, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import httpx_client

PLATFORMS = [
    Platform.SWITCH,
]

type TriggercmdConfigEntry = ConfigEntry[ha.Hub]


async def async_setup_entry(hass: UniversalAssistant, entry: TriggercmdConfigEntry) -> None:
    """Set up TRIGGERcmd from a config entry."""
    hass_client = httpx_client.get_async_client(hass)
    hub = ha.Hub(entry.data[CONF_TOKEN])
    await hub.async_init(hass_client)
    status_code = await client.async_connection_test(
        entry.data[CONF_TOKEN], hass_client
    )
    if status_code != 200:
        raise ConfigEntryNotReady

    entry.runtime_data = hub
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: TriggercmdConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
