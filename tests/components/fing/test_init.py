"""Test the Fing integration init."""

import pytest
from pytest_universalassistant.common import AsyncMock
from pytest_universalassistant.plugins import MockConfigEntry

from universalassistant.components.fing.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import init_integration


@pytest.mark.parametrize("api_type", ["new", "old"])
async def test_setup_entry_new_api(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mocked_fing_agent: AsyncMock,
    api_type: str,
) -> None:
    """Test setup Fing Agent /w New API."""
    entry = await init_integration(hass, mock_config_entry, mocked_fing_agent)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    if api_type == "new":
        assert entry.state is ConfigEntryState.LOADED
    elif api_type == "old":
        assert entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.parametrize("api_type", ["new"])
async def test_unload_entry(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mocked_fing_agent: AsyncMock,
) -> None:
    """Test unload of entry."""
    entry = await init_integration(hass, mock_config_entry, mocked_fing_agent)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
