"""Tests for the Fing integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry, mocked_fing_agent
) -> MockConfigEntry:
    """Set up Fing integration for testing."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    return config_entry
