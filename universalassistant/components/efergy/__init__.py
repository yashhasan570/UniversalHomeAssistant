"""The Efergy integration."""

from pyefergy import Efergy, exceptions

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_API_KEY, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

PLATFORMS = [Platform.SENSOR]
type EfergyConfigEntry = ConfigEntry[Efergy]


async def async_setup_entry(hass: UniversalAssistant, entry: EfergyConfigEntry) -> None:
    """Set up Efergy from a config entry."""
    api = Efergy(
        entry.data[CONF_API_KEY],
        session=async_get_clientsession(hass),
        utc_offset=hass.config.time_zone,
        currency=hass.config.currency,
    )

    try:
        await api.async_status(get_sids=True)
    except (exceptions.ConnectError, exceptions.DataError) as ex:
        raise ConfigEntryNotReady(f"Failed to connect to device: {ex}") from ex
    except exceptions.InvalidAuth as ex:
        raise ConfigEntryAuthFailed(
            "API Key is no longer valid. Please reauthenticate"
        ) from ex

    entry.runtime_data = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: EfergyConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
