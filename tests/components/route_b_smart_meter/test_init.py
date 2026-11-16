"""Tests for the Smart Meter B Route integration init."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.route_b_smart_meter.const import (
    CONNECT_RETRIES,
    REOPEN_DELAYS,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant


async def test_async_setup_entry_success(
    hass: UniversalAssistant, mock_momonga, mock_config_entry: MockConfigEntry
) -> None:
    """Test successful setup of entry."""
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED
    kwargs = mock_momonga.call_args.kwargs
    assert kwargs["reopen_delays"] == REOPEN_DELAYS
    assert kwargs["scan_retries"] == CONNECT_RETRIES
    assert kwargs["join_retries"] == CONNECT_RETRIES

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
