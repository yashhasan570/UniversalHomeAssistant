"""Tests for the Sense integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.sense.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def setup_platform(
    hass: UniversalAssistant, config_entry: MockConfigEntry, platform: Platform
) -> MockConfigEntry:
    """Set up the Sense platform."""
    config_entry.add_to_hass(hass)

    with patch("universalassistant.components.sense.PLATFORMS", [platform]):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return config_entry
