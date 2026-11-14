"""Tests for the awair component."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.awair.const import DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def setup_awair(hass: __HAC_KEEP__, fixtures, unique_id, data) -> ConfigEntry:
    """Add Awair devices to hass, using specified fixtures for data."""

    entry = MockConfigEntry(domain=DOMAIN, unique_id=unique_id, data=data)
    with patch("python_awair.AwairClient.query", side_effect=fixtures):
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
