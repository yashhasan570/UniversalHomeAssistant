"""The igloohome integration."""

from dataclasses import dataclass

from aiohttp import ClientError
from igloohome_api import (
    Api as IgloohomeApi,
    ApiException,
    Auth as IgloohomeAuth,
    AuthException,
    GetDeviceInfoResponse,
)

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

PLATFORMS: list[Platform] = [Platform.LOCK, Platform.SENSOR]


@dataclass
class IgloohomeRuntimeData:
    """Holding class for runtime data."""

    api: IgloohomeApi
    devices: list[GetDeviceInfoResponse]


type IgloohomeConfigEntry = ConfigEntry[IgloohomeRuntimeData]


async def async_setup_entry(hass: UniversalAssistant, entry: IgloohomeConfigEntry) -> None:
    """Set up igloohome from a config entry."""
    authentication = IgloohomeAuth(
        session=async_get_clientsession(hass),
        client_id=entry.data[CONF_CLIENT_ID],
        client_secret=entry.data[CONF_CLIENT_SECRET],
    )

    api = IgloohomeApi(auth=authentication)
    try:
        devices = (await api.get_devices()).payload
    except AuthException as e:
        raise ConfigEntryError from e
    except (ApiException, ClientError) as e:
        raise ConfigEntryNotReady from e

    entry.runtime_data = IgloohomeRuntimeData(api, devices)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: IgloohomeConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
