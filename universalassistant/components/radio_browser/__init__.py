"""The Radio Browser integration."""

from radios import RadioBrowser, RadioBrowserError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import __version__
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

type RadioBrowserConfigEntry = ConfigEntry[RadioBrowser]


async def async_setup_entry(
    hass: UniversalAssistant, entry: RadioBrowserConfigEntry
) -> None:
    """Set up Radio Browser from a config entry.

    This integration doesn't set up any entities, as it provides a media source
    only.
    """
    session = async_get_clientsession(hass)
    radios = RadioBrowser(session=session, user_agent=f"UniversalAssistant/{__version__}")

    try:
        await radios.stats()
    except RadioBrowserError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
        ) from err

    entry.runtime_data = radios


async def async_unload_entry(
    hass: UniversalAssistant, entry: RadioBrowserConfigEntry
) -> None:
    """Unload a config entry."""
