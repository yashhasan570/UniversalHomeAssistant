"""Tests for the Roomba integration setup."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from roombapy import RoombaAuthError, RoombaConnectionError

from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(RoombaConnectionError, id="unreachable"),
        pytest.param(RoombaAuthError, id="rejected_password"),
    ],
)
async def test_setup_retry_on_connect_error(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_roomba: AsyncMock,
    error: type[Exception],
) -> None:
    """Test that a failed connection schedules a retry."""
    mock_roomba.connect.side_effect = error

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_disconnects(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_roomba: AsyncMock,
) -> None:
    """Test that unloading the entry closes the connection."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    mock_roomba.connect.assert_awaited_once()

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
    mock_roomba.disconnect.assert_awaited_once()


async def test_stop_disconnects(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_roomba: AsyncMock,
) -> None:
    """Test that stopping __HA_KEEP__ closes the connection."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done()

    mock_roomba.disconnect.assert_awaited_once()


@pytest.mark.usefixtures("mock_roomba")
async def test_setup_cannot_connect(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test setup fails when no connection data is returned."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.roomba.async_connect_or_timeout",
        return_value={},
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    assert mock_config_entry.reason == "Failed to connect to Roomba at 192.168.0.30"
