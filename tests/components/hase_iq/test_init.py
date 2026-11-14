"""Tests for the Hase iQ setup and teardown."""

from unittest.mock import MagicMock

from pyhaseiq import ConnectionFailedError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


@pytest.mark.usefixtures("mock_client")
async def test_setup_and_unload(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test the entry loads and unloads."""
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_retry(
    hass: __HAC_KEEP__, mock_client: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test an unreachable stove puts the entry in retry."""
    mock_client.get_status.side_effect = ConnectionFailedError("unreachable")

    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
