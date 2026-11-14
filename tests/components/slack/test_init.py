"""Test Slack integration."""

from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.slack.const import DOMAIN
from universalassistant.config_entries import SOURCE_REAUTH, ConfigEntry, ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import CONF_DATA, async_init_integration


async def test_setup(hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker) -> None:
    """Test Slack setup."""
    entry: ConfigEntry = await async_init_integration(hass, aioclient_mock)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.data == CONF_DATA


async def test_async_setup_entry_not_ready(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test that it throws ConfigEntryNotReady when exception occurs during setup."""
    entry: ConfigEntry = await async_init_integration(
        hass, aioclient_mock, error="cannot_connect"
    )
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_async_setup_entry_invalid_auth(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test invalid auth during setup."""
    entry: ConfigEntry = await async_init_integration(
        hass, aioclient_mock, error="invalid_auth"
    )
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Invalid API key"

    flows = hass.config_entries.flow.async_progress()
    assert len(flows) == 1
    assert flows[0]["context"]["source"] == SOURCE_REAUTH
    assert flows[0]["context"]["entry_id"] == entry.entry_id
