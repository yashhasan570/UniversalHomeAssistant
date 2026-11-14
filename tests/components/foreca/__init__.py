"""Tests for the Foreca integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__


async def init_integration(hass: __HAC_KEEP__, entry: MockConfigEntry) -> None:
    """Set up the Foreca integration for testing."""
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
