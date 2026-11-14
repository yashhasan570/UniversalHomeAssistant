"""The seventeentrack component."""

from pyseventeentrack import Client as SeventeenTrackClient
from pyseventeentrack.errors import SeventeenTrackError

from universalassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.aiohttp_client import async_create_clientsession
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import SeventeenTrackConfigEntry, SeventeenTrackCoordinator
from .services import async_setup_services

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the 17Track component."""

    async_setup_services(hass)

    return True


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: SeventeenTrackConfigEntry
) -> None:
    """Set up 17Track from a config entry."""

    session = async_create_clientsession(hass)
    client = SeventeenTrackClient(session=session)

    try:
        await client.profile.login(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    except SeventeenTrackError as err:
        raise ConfigEntryNotReady from err

    seventeen_coordinator = SeventeenTrackCoordinator(hass, entry, client)

    await seventeen_coordinator.async_config_entry_first_refresh()

    entry.runtime_data = seventeen_coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
