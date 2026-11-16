"""Test the EnOcean integration."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant


async def test_device_not_connected(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test that a config entry is not ready if the device is not connected."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.enocean.Gateway.start",
        side_effect=ConnectionError("Device not found"),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_stops_gateway(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, mock_gateway: Mock
) -> None:
    """Test that unloading the config entry stops the gateway."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
    mock_gateway.stop.assert_awaited_once()
