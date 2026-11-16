"""Tests for the V2C integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def init_integration(
    hass: UniversalAssistant, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the V2C integration in Universal Home Assistant."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
