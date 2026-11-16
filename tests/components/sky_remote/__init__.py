"""Tests for the Sky Remote component."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_mock_entry(hass: UniversalAssistant, entry: MockConfigEntry):
    """Initialize a mock config entry."""
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()
