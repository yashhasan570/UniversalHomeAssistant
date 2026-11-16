"""Utils for Vodafone Station."""

from aiohttp import ClientSession, CookieJar

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import aiohttp_client


async def async_client_session(hass: UniversalAssistant) -> ClientSession:
    """Return a new aiohttp session."""
    return aiohttp_client.async_create_clientsession(
        hass, verify_ssl=False, cookie_jar=CookieJar(unsafe=True, quote_cookie=False)
    )
