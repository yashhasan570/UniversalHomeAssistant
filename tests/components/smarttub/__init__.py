"""Tests for the smarttub integration."""

from datetime import timedelta

from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.components.smarttub.const import SCAN_INTERVAL
from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util


async def trigger_update(hass: UniversalAssistant) -> None:
    """Trigger a polling update by moving time forward."""
    new_time = dt_util.utcnow() + timedelta(seconds=SCAN_INTERVAL + 1)
    async_fire_time_changed(hass, new_time)
    await hass.async_block_till_done(wait_background_tasks=True)
