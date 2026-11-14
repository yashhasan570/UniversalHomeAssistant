"""Tests for the V2C integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the V2C integration in __HA_KEEP__."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
