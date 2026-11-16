"""The HVV integration."""

from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import aiohttp_client

from .hub import GTIHub, HVVConfigEntry

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: HVVConfigEntry) -> None:
    """Set up HVV from a config entry."""

    hub = GTIHub(
        entry.data[CONF_HOST],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        aiohttp_client.async_get_clientsession(hass),
    )

    entry.runtime_data = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: HVVConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
