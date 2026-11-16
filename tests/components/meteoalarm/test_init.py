"""Tests for the MeteoAlarm integration setup."""

from unittest.mock import MagicMock

from meteoalarmapi import ServerError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant


async def test_setup_and_unload(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meteoalert: MagicMock,
) -> None:
    """Test the entry is set up and unloaded."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_retry_when_unreachable(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meteoalert: MagicMock,
) -> None:
    """Test setup is retried when MeteoAlarm can't be reached at startup."""
    mock_meteoalert.return_value.get_alert.side_effect = ServerError("500")
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
