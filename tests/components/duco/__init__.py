"""Tests for the Duco integration."""

from collections.abc import Sequence
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.duco.const import SCAN_INTERVAL
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


async def async_fire_coordinator_update(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Trigger a scheduled coordinator update."""
    freezer.tick(SCAN_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)


async def setup_integration(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> MockConfigEntry:
    """Set up the full Duco integration for testing."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry


async def setup_platform_integration(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    platforms: Sequence[Platform],
) -> MockConfigEntry:
    """Set up selected Duco platforms for testing."""
    config_entry.add_to_hass(hass)
    with patch("universalassistant.components.duco.PLATFORMS", list(platforms)):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
    return config_entry
