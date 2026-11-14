"""Tests for the PoolSense integration setup."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


async def test_setup_invalid_auth(
    hass: __HAC_KEEP__,
    mock_poolsense_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup fails with invalid credentials."""
    mock_poolsense_client.test_poolsense_credentials.return_value = False

    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    assert mock_config_entry.reason == "Invalid authentication"
