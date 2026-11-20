"""Tests for the Tile BLE integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_load_unload(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test the config entry loads without the Tile in range and unloads."""
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
