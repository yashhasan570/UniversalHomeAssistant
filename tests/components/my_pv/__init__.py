"""The tests for the my-PV component."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant

ELWA2_SERIAL_NUMBER = "1601500000000000"


async def setup_integration(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """Set up the my-PV integration."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
