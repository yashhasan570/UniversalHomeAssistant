"""Tests for the LED Infrared integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


async def test_setup_and_unload_entry(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry
) -> None:
    """Test setting up and unloading a config entry."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.NOT_LOADED
