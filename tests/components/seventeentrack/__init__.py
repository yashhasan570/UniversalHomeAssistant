"""Tests for the seventeentrack component."""

from datetime import timedelta

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.seventeentrack.const import DEFAULT_SCAN_INTERVAL
from universalassistant.core import __HAC_KEEP__


async def init_integration(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> None:
    """Set up the 17Track integration in __HA_KEEP__."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


async def goto_future(hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory):
    """Move to future."""
    freezer.tick(DEFAULT_SCAN_INTERVAL + timedelta(minutes=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
