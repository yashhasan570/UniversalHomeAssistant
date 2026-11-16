"""Tests for the DirecTV integration."""

from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_config_entry_not_ready(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test the DirecTV configuration entry not ready."""
    entry = await setup_integration(hass, aioclient_mock, setup_error=True)

    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_config_entry(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test the DirecTV configuration entry unloading."""
    entry = await setup_integration(hass, aioclient_mock)

    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
