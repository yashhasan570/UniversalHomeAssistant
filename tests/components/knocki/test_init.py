"""Test the Home Knocki init module."""

from unittest.mock import AsyncMock

from knocki import KnockiConnectionError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_load_unload_entry(
    hass: UniversalAssistant,
    mock_knocki_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test load and unload entry."""
    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_remove(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_initialization_failure(
    hass: UniversalAssistant,
    mock_knocki_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test initialization failure."""
    mock_knocki_client.get_triggers.side_effect = KnockiConnectionError

    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
    assert mock_config_entry.error_reason_translation_key == "update_error"
