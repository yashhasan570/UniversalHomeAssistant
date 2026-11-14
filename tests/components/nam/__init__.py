"""Tests for the Nettigo Air Monitor integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_integration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Set up the Nettigo Air Monitor integration for testing."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
