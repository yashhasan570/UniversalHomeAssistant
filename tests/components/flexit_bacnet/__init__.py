"""Tests for the Flexit Nordic (BACnet) integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant


async def setup_with_selected_platforms(
    hass: UniversalAssistant, entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Set up the Flexit Nordic (BACnet) integration with the selected platforms."""
    entry.add_to_hass(hass)
    with patch("universalassistant.components.flexit_bacnet.PLATFORMS", platforms):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
