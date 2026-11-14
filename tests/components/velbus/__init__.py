"""Tests for the Velbus component."""

from universalassistant.components.velbus import VelbusConfigEntry
from universalassistant.core import UniversalAssistant


async def init_integration(
    hass: UniversalAssistant,
    config_entry: VelbusConfigEntry,
) -> None:
    """Load the Velbus integration."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
