"""Tests for the Hydro-Québec Peak Events integration setup."""

from unittest.mock import MagicMock

from hydropeak_opendata import OpenDataConnectionError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


async def test_setup_and_unload(
    hass: __HAC_KEEP__,
    mock_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test a successful setup and unload."""
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_retry_on_error(
    hass: __HAC_KEEP__,
    mock_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the entry goes to setup retry when the feed is unavailable."""
    mock_client.get_events.side_effect = OpenDataConnectionError("boom")

    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
