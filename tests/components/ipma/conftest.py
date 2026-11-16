"""Define test fixtures for IPMA."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.ipma.const import DOMAIN
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from universalassistant.core import UniversalAssistant

from . import MockLocation


@pytest.fixture
def config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Define a config entry fixture."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_NAME: "Home",
            CONF_LATITUDE: 0,
            CONF_LONGITUDE: 0,
        },
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
async def init_integration(
    hass: UniversalAssistant, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the IPMA integration for testing."""
    config_entry.add_to_hass(hass)

    with patch("pyipma.location.Location.get", return_value=MockLocation()):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        return config_entry
