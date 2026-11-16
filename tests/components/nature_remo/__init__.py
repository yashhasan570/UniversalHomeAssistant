"""Tests for the Nature Remo integration."""

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.components.nature_remo.const import UPDATE_INTERVAL
from universalassistant.core import UniversalAssistant


async def async_poll(hass: UniversalAssistant, freezer: FrozenDateTimeFactory) -> None:
    """Advance time to the next coordinator poll and let it settle."""
    freezer.tick(UPDATE_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
