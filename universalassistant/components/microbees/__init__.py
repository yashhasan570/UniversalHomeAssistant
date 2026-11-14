"""The microBees integration."""

from dataclasses import dataclass
from http import HTTPStatus
import logging

import aiohttp
from microBeesPy import MicroBees

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers import config_entry_oauth2_flow

from .const import PLATFORMS
from .coordinator import MicroBeesUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


type MicroBeesConfigEntry = ConfigEntry[__HAC_KEEP__MicroBeesData]


@dataclass(frozen=True, kw_only=True)
class __HAC_KEEP__MicroBeesData:
    """Microbees data stored in the config entry runtime_data."""

    connector: MicroBees
    coordinator: MicroBeesUpdateCoordinator
    session: config_entry_oauth2_flow.OAuth2Session


async def async_migrate_entry(hass: __HAC_KEEP__, entry: MicroBeesConfigEntry) -> None:
    """Migrate entry."""
    _LOGGER.debug("Migrating from version %s.%s", entry.version, entry.minor_version)

    if entry.version == 1:
        # 1 -> 1.2: Unique ID from integer to string
        if entry.minor_version == 1:
            minor_version = 2
            hass.config_entries.async_update_entry(
                entry, unique_id=str(entry.unique_id), minor_version=minor_version
            )

    _LOGGER.debug("Migration successful")


async def async_setup_entry(hass: __HAC_KEEP__, entry: MicroBeesConfigEntry) -> None:
    """Set up microBees from a config entry."""
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    try:
        await session.async_ensure_token_valid()
    except aiohttp.ClientResponseError as ex:
        if ex.status in (
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        ):
            raise ConfigEntryAuthFailed("Token not valid, trigger renewal") from ex
        raise ConfigEntryNotReady from ex
    microbees = MicroBees(token=session.token[CONF_ACCESS_TOKEN])
    coordinator = MicroBeesUpdateCoordinator(hass, entry, microbees)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = __HAC_KEEP__MicroBeesData(
        connector=microbees,
        coordinator=coordinator,
        session=session,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: MicroBeesConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
