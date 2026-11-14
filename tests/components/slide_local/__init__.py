"""Tests for the slide_local integration."""

from typing import Any
from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry, load_json_object_fixture

from universalassistant.components.slide_local.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant


async def setup_platform(
    hass: UniversalAssistant, config_entry: MockConfigEntry, platforms: list[Platform]
) -> MockConfigEntry:
    """Set up the slide local integration."""
    config_entry.add_to_hass(hass)

    with patch("universalassistant.components.slide_local.PLATFORMS", platforms):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    return config_entry


def get_data() -> dict[str, Any]:
    """Return the default state data.

    The coordinator mutates the returned API data, so we can't return a glocal dict.
    """
    return load_json_object_fixture("slide_1.json", DOMAIN)
