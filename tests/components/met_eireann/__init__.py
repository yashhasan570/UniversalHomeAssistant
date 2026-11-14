"""Tests for Met Éireann."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.met_eireann.const import DOMAIN
from universalassistant.const import (
    CONF_ELEVATION,
    CONF_LATITUDE,
    CONF_LOCATION,
    CONF_LONGITUDE,
    CONF_NAME,
)
from universalassistant.core import __HAC_KEEP__


async def init_integration(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Set up the Met Éireann integration in __HA_KEEP__."""
    entry_data = {
        CONF_NAME: "test",
        CONF_LOCATION: {
            CONF_LATITUDE: 0,
            CONF_LONGITUDE: 0,
        },
        CONF_ELEVATION: 0,
    }
    entry = MockConfigEntry(domain=DOMAIN, data=entry_data, version=2)
    with patch(
        "universalassistant.components.met_eireann.coordinator.meteireann.WeatherData.fetching_data",
        return_value=True,
    ):
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
