"""Tests for the Nina integration."""

from copy import deepcopy
from unittest.mock import AsyncMock, patch

from pynina import Warning
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.nina.const import CONF_REGIONS
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


async def setup_platform(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    mock_nina_class: AsyncMock,
    nina_warnings: list[Warning],
) -> None:
    """Set up the NINA platforms."""
    mock_nina_class.warnings = {
        region: deepcopy(nina_warnings)
        for region in config_entry.data.get(CONF_REGIONS, {})
    }

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED


async def setup_single_platform(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    platform: Platform | None,
    mock_nina_class: AsyncMock,
    nina_warnings: list[Warning],
) -> None:
    """Set up a single NINA platform."""
    mock_nina_class.warnings = {
        region: deepcopy(nina_warnings)
        for region in config_entry.data.get(CONF_REGIONS, {})
    }

    platforms = [platform] if platform else []

    with patch("universalassistant.components.nina.PLATFORMS", platforms):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED
