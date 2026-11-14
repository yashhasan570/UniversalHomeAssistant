"""The loqed integration."""

import re

import aiohttp
from loqedAPI import loqed

from universalassistant.components import cloud
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import LoqedConfigEntry, LoqedDataCoordinator, is_auth_error

PLATFORMS: list[Platform] = [Platform.LOCK, Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: LoqedConfigEntry) -> None:
    """Set up loqed from a config entry."""
    websession = async_get_clientsession(hass)
    host = entry.data["bridge_ip"]
    apiclient = loqed.APIClient(websession, f"http://{host}")
    api = loqed.LoqedAPI(apiclient)

    try:
        lock = await api.async_get_lock(
            entry.data["lock_key_key"],
            entry.data["bridge_key"],
            int(entry.data["lock_key_local_id"]),
            re.sub(
                r"LOQED-([a-f0-9]+)\.local", r"\1", entry.data["bridge_mdns_hostname"]
            ),
        )
    except (
        TimeoutError,
        aiohttp.ClientError,
    ) as ex:
        if is_auth_error(ex):
            raise ConfigEntryAuthFailed(
                f"The bridge at {host} rejected the credentials"
            ) from ex
        raise ConfigEntryNotReady(f"Unable to connect to bridge at {host}") from ex
    coordinator = LoqedDataCoordinator(hass, entry, api, lock)

    try:
        await coordinator.ensure_webhooks()
    except (TimeoutError, aiohttp.ClientError) as ex:
        if is_auth_error(ex):
            raise ConfigEntryAuthFailed(
                f"The bridge at {host} rejected the credentials"
            ) from ex
        raise ConfigEntryNotReady(f"Unable to connect to bridge at {host}") from ex
    except cloud.CloudNotAvailable as ex:
        raise ConfigEntryNotReady(
            "Unable to create __HA_KEEP__ Cloud webhook"
        ) from ex

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: LoqedConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    await entry.runtime_data.remove_webhooks()
