"""Tests for the Vegetronix VegeHub integration."""

from universalassistant.components.vegehub.coordinator import VegeHubConfigEntry
from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__,
    config_entry: VegeHubConfigEntry,
) -> None:
    """Load the VegeHub integration."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
