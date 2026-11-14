"""Define notion utilities."""

from aionotion import (
    async_get_client_with_credentials as cwc,
    async_get_client_with_refresh_token as cwrt,
)
from aionotion.client import Client

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import aiohttp_client
from universalassistant.helpers.instance_id import async_get


async def async_get_client_with_credentials(
    hass: __HAC_KEEP__, email: str, password: str
) -> Client:
    """Get a Notion client with credentials."""
    session = aiohttp_client.async_get_clientsession(hass)
    instance_id = await async_get(hass)
    return await cwc(email, password, session=session, session_name=instance_id)


async def async_get_client_with_refresh_token(
    hass: __HAC_KEEP__, user_uuid: str, refresh_token: str
) -> Client:
    """Get a Notion client with credentials."""
    session = aiohttp_client.async_get_clientsession(hass)
    instance_id = await async_get(hass)
    return await cwrt(
        user_uuid, refresh_token, session=session, session_name=instance_id
    )
