"""Tests for the Monzo API."""

from universalassistant.components.monzo.api import MonzoAPI
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession


async def test_access_token(hass: UniversalAssistant) -> None:
    """Test returning a static access token."""
    api = MonzoAPI(async_get_clientsession(hass), "access-token")

    assert await api.async_get_access_token() == "access-token"
