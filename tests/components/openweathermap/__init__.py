"""Shared utilities for OpenWeatherMap tests."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


async def setup_platform(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    platforms: list[Platform],
):
    """Set up the OpenWeatherMap platform."""
    config_entry.add_to_hass(hass)
    with (
        patch("universalassistant.components.openweathermap.PLATFORMS", platforms),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED
