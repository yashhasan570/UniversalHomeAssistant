"""Tests for the NextDNS integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def init_integration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Set up the NextDNS integration in Universal Home Assistant."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
