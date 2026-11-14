"""Tests for the API component of the Home Connect integration."""

from unittest.mock import MagicMock

from aiohomeconnect.const import API_ENDPOINT
import pytest

from universalassistant.components.home_connect.api import AsyncConfigEntryAuth
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_oauth2_flow


@pytest.mark.parametrize("country", ["CN", "ES"])
async def test_regional_api_endpoint(hass: __HAC_KEEP__, country: str) -> None:
    """Test that the API endpoint is set correctly based on the country."""
    hass.config.country = country
    oauth_session = MagicMock(spec=config_entry_oauth2_flow.OAuth2Session)
    auth = AsyncConfigEntryAuth(hass, oauth_session)

    expected_endpoint = (
        API_ENDPOINT if country != "CN" else API_ENDPOINT.replace(".com", ".cn")
    )
    assert auth.host == expected_endpoint
