"""Tests for the Flipr integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_integration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Fixture for setting up the component."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
