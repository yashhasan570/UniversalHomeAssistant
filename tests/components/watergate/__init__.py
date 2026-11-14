"""Tests for the Watergate integration."""

from universalassistant.core import __HAC_KEEP__


async def init_integration(hass: __HAC_KEEP__, mock_entry) -> None:
    """Set up the Watergate integration in __HA_KEEP__."""
    mock_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
