"""Test the Met Éireann integration init."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.met_eireann.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import (
    CONF_ELEVATION,
    CONF_LATITUDE,
    CONF_LOCATION,
    CONF_LONGITUDE,
    CONF_NAME,
)
from universalassistant.core import UniversalAssistant

from . import init_integration


async def test_unload_entry(hass: UniversalAssistant) -> None:
    """Test successful unload of entry."""
    entry = await init_integration(hass)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)


async def test_migrate_entry(hass: UniversalAssistant) -> None:
    """Test entry migration."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_NAME: "test",
            CONF_LATITUDE: 0,
            CONF_LONGITUDE: 0,
            CONF_ELEVATION: 0,
        },
        version=1,
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.met_eireann.coordinator.meteireann.WeatherData.fetching_data",
        return_value=True,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    assert entry.version == 2
    assert entry.data == {
        CONF_NAME: "test",
        CONF_LOCATION: {
            CONF_LATITUDE: 0,
            CONF_LONGITUDE: 0,
        },
        CONF_ELEVATION: 0,
    }
