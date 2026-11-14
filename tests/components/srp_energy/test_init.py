"""Tests for Srp Energy component Init."""

from universalassistant.components.recorder import Recorder
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


async def test_setup_entry(
    recorder_mock: Recorder, hass: __HAC_KEEP__, init_integration
) -> None:
    """Test setup entry."""
    assert init_integration.state is ConfigEntryState.LOADED


async def test_unload_entry(
    recorder_mock: Recorder, hass: __HAC_KEEP__, init_integration
) -> None:
    """Test being able to unload an entry."""
    assert init_integration.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(init_integration.entry_id)
    await hass.async_block_till_done()
