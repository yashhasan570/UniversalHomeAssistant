"""Tests for Bravia TV."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Set up the Bravia TV integration in __HA_KEEP__."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
