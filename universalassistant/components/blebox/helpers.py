"""Blebox helpers."""

import aiohttp

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import (
    async_create_clientsession,
    async_get_clientsession,
)


def get_maybe_authenticated_session(
    hass: UniversalAssistant, password: str | None, username: str | None
) -> aiohttp.ClientSession:
    """Return proper session object."""
    if username and password:
        return async_create_clientsession(
            hass,
            headers={"Authorization": aiohttp.encode_basic_auth(username, password)},
        )

    return async_get_clientsession(hass)
