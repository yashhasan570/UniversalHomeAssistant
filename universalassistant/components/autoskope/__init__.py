"""The Autoskope integration."""

import aiohttp
from autoskope_client.api import AutoskopeApi
from autoskope_client.models import CannotConnect, InvalidAuth

from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DEFAULT_HOST
from .coordinator import AutoskopeConfigEntry, AutoskopeDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: UniversalAssistant, entry: AutoskopeConfigEntry) -> None:
    """Set up Autoskope from a config entry."""
    session = async_create_clientsession(hass, cookie_jar=aiohttp.CookieJar())

    api = AutoskopeApi(
        host=entry.data.get(CONF_HOST, DEFAULT_HOST),
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=session,
    )

    try:
        await api.connect()
    except InvalidAuth as err:
        raise ConfigEntryAuthFailed(
            "Authentication failed, please check credentials"
        ) from err
    except CannotConnect as err:
        raise ConfigEntryNotReady("Could not connect to Autoskope API") from err

    coordinator = AutoskopeDataUpdateCoordinator(hass, api, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AutoskopeConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
