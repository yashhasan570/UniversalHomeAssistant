"""Tests for the bsblan integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


async def setup_with_selected_platforms(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Set up the BSBLAN integration with the selected platforms."""
    config_entry.add_to_hass(hass)
    with patch("universalassistant.components.bsblan.PLATFORMS", platforms):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
