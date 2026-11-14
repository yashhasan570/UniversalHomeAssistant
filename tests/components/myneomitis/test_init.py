"""Tests for the MyNeomitis integration."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import __HAC_KEEP__


async def test_minimal_setup(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """Test the minimal setup of the MyNeomitis integration."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED


async def test_setup_entry_raises_on_login_fail(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """Test that async_setup_entry sets entry to retry if login fails."""
    mock_pyaxenco_client.login.side_effect = TimeoutError("fail-login")

    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_entry_success(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """Test that unloading via hass.config_entries.async_unload disconnects cleanly."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)

    mock_pyaxenco_client.disconnect_websocket.assert_awaited_once()


async def test_unload_entry_logs_on_disconnect_error(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """When disconnecting the websocket fails, an error is logged."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    mock_pyaxenco_client.disconnect_websocket.side_effect = TimeoutError("to")

    caplog.set_level("ERROR")
    result = await hass.config_entries.async_unload(mock_config_entry.entry_id)

    assert result is True
    assert "Error while disconnecting WebSocket" in caplog.text


async def test_universalassistant_stop_disconnects_websocket(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """Test that WebSocket is disconnected on __HA_KEEP__ stop event."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done()

    mock_pyaxenco_client.disconnect_websocket.assert_awaited_once()


async def test_universalassistant_stop_logs_on_disconnect_error(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
    mock_config_entry: MockConfigEntry,
    mock_pyaxenco_client: AsyncMock,
) -> None:
    """Test that WebSocket disconnect errors are logged on HA stop."""
    mock_pyaxenco_client.disconnect_websocket.side_effect = TimeoutError(
        "disconnect failed"
    )

    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    caplog.set_level("ERROR")

    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done()

    assert "Error while disconnecting WebSocket" in caplog.text
