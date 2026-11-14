"""The lg_netcast component."""

from typing import Final

from pylgnetcast import LgNetCastClient

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_HOST, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv

from .const import DOMAIN

PLATFORMS: Final[list[Platform]] = [Platform.MEDIA_PLAYER, Platform.REMOTE]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type LgNetCastConfigEntry = ConfigEntry[LgNetCastClient]


async def async_setup_entry(
    hass: __HAC_KEEP__, config_entry: LgNetCastConfigEntry
) -> None:
    """Set up a config entry."""
    host = config_entry.data[CONF_HOST]
    access_token = config_entry.data[CONF_ACCESS_TOKEN]

    client = LgNetCastClient(host, access_token)

    config_entry.runtime_data = client

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: LgNetCastConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
