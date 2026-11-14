"""Tests for the israel_rail component."""

from datetime import timedelta

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.israel_rail.const import DEFAULT_SCAN_INTERVAL
from universalassistant.core import UniversalAssistant


async def init_integration(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """Set up the israel rail integration in Universal Universal Home Assistant."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


async def goto_future(hass: UniversalAssistant, freezer: FrozenDateTimeFactory):
    """Move to future."""
    freezer.tick(DEFAULT_SCAN_INTERVAL + timedelta(minutes=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
