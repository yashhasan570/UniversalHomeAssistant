"""Tests for the Gree Infrared integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant


async def test_setup_and_unload_entry(
    hass: UniversalAssistant, init_integration: MockConfigEntry
) -> None:
    """Test setting up and unloading a config entry."""
    entry = init_integration
    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
