"""Tests for the Fyta integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant


async def setup_platform(
    hass: UniversalAssistant, config_entry: MockConfigEntry, platforms: list[Platform]
) -> MockConfigEntry:
    """Set up the Fyta platform."""
    config_entry.add_to_hass(hass)

    with patch("universalassistant.components.fyta.PLATFORMS", platforms):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
