"""Test the Helty Flow setup."""

from unittest.mock import AsyncMock

from pyhelty import HeltyConnectionError, HeltyResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


async def test_setup_and_unload(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test a config entry sets up and tears down cleanly."""
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


@pytest.mark.parametrize("side_effect", [HeltyConnectionError, HeltyResponseError])
async def test_setup_error(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    side_effect: type[Exception],
) -> None:
    """Test an error talking to the unit during setup leads to a retry."""
    mock_helty_client.async_get_data.side_effect = side_effect

    mock_config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
