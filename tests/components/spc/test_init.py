"""Tests for Vanderbilt SPC component."""

from unittest.mock import AsyncMock

from universalassistant.components.spc import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_valid_device_config(hass: __HAC_KEEP__, mock_client: AsyncMock) -> None:
    """Test valid device config."""
    config = {"spc": {"api_url": "http://localhost/", "ws_url": "ws://localhost/"}}

    assert await async_setup_component(hass, DOMAIN, config) is True


async def test_invalid_device_config(
    hass: __HAC_KEEP__, mock_client: AsyncMock
) -> None:
    """Test valid device config."""
    config = {"spc": {"api_url": "http://localhost/"}}

    assert await async_setup_component(hass, DOMAIN, config) is False
