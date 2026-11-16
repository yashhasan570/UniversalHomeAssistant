"""Test init."""

from unittest.mock import MagicMock

import httpx2
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.iotawatt.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from . import INPUT_SENSOR


async def test_setup_unload(
    hass: UniversalAssistant, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test we can setup and unload an entry."""
    mock_iotawatt.getSensors.return_value["sensors"]["my_sensor_key"] = INPUT_SENSOR
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert await hass.config_entries.async_unload(entry.entry_id)


async def test_setup_connection_failed(
    hass: UniversalAssistant, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test connection error during startup."""
    mock_iotawatt.connect.side_effect = httpx2.ConnectError("")
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_auth_failed(
    hass: UniversalAssistant, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test auth error during startup."""
    mock_iotawatt.connect.return_value = False
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_update_failed(
    hass: UniversalAssistant, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test error while fetching sensor data during startup."""
    mock_iotawatt.update.side_effect = httpx2.HTTPStatusError(
        "", request=MagicMock(), response=MagicMock()
    )
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY
