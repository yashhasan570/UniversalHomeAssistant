"""Blebox helpers tests."""

from aiohttp import encode_basic_auth
from aiohttp.hdrs import AUTHORIZATION

from universalassistant.components.blebox.helpers import get_maybe_authenticated_session
from universalassistant.core import UniversalAssistant


async def test_get_maybe_authenticated_session_none(hass: UniversalAssistant) -> None:
    """Tests if the session has no authorization header."""
    session = get_maybe_authenticated_session(hass=hass, username="", password="")
    assert AUTHORIZATION not in session.headers


async def test_get_maybe_authenticated_session_auth(hass: UniversalAssistant) -> None:
    """Tests if the session has a basic authorization header."""
    session = get_maybe_authenticated_session(
        hass=hass, username="user", password="password"
    )
    assert session.headers[AUTHORIZATION] == encode_basic_auth("user", "password")
