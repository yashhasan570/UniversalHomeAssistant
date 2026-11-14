"""Tests for the buienradar component."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.buienradar.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__

TEST_LATITUDE = 51.5288504
TEST_LONGITUDE = 5.4002156


async def test_load_unload(
    aioclient_mock: AiohttpClientMocker, hass: __HAC_KEEP__
) -> None:
    """Test options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_LATITUDE: TEST_LATITUDE,
            CONF_LONGITUDE: TEST_LONGITUDE,
        },
        unique_id=DOMAIN,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
