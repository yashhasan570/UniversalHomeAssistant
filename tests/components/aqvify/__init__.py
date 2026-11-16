"""Tests for Aqvify integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_integration(hass: UniversalAssistant, config_entry: MockConfigEntry) -> None:
    """Helper for setting up the component."""

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
