"""Tests for the Velbus component."""

from universalassistant.components.velbus import VelbusConfigEntry
from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__,
    config_entry: VelbusConfigEntry,
) -> None:
    """Load the Velbus integration."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
