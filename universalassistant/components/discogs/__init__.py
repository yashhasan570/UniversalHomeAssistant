"""The Discogs integration."""

import discogs_client

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_TOKEN
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import SERVER_SOFTWARE

from .const import PLATFORMS

type DiscogsConfigEntry = ConfigEntry[discogs_client.Client]


async def async_setup_entry(hass: __HAC_KEEP__, entry: DiscogsConfigEntry) -> None:
    """Set up Discogs from a config entry."""

    def _setup_client() -> discogs_client.Client:
        client = discogs_client.Client(
            SERVER_SOFTWARE, user_token=entry.data[CONF_TOKEN]
        )
        client.identity()
        return client

    try:
        client = await hass.async_add_executor_job(_setup_client)
    except discogs_client.exceptions.HTTPError as err:
        raise ConfigEntryNotReady(f"Error communicating with Discogs: {err}") from err

    entry.runtime_data = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: DiscogsConfigEntry) -> None:
    """Unload Discogs config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
