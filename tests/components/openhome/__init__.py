"""Tests for the Linn / OpenHome integration."""

from datetime import timedelta

from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.core import __HAC_KEEP__
from universalassistant.util import dt as dt_util


async def setup_integration(hass: __HAC_KEEP__, config_entry: MockConfigEntry) -> None:
    """Set up the openhome integration."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


async def async_poll(hass: __HAC_KEEP__) -> None:
    """Trigger a poll of the polling platforms.

    Well past the media player's ten second scan interval.
    """
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=30))
    await hass.async_block_till_done()
