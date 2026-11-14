"""Tests for Airly."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def init_integration(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """Set up the Airly integration in Universal Universal Home Assistant."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
