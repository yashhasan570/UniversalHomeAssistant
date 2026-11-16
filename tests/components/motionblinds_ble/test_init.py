"""Tests for Motionblinds BLE init."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info

from universalassistant.components.bluetooth.models import BluetoothServiceInfoBleak
from universalassistant.components.motionblinds_ble import options_update_listener
from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_options_update_listener(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test options_update_listener."""

    await setup_integration(hass, mock_config_entry)

    with (
        patch(
            "universalassistant.components.motionblinds_ble.MotionDevice.set_custom_disconnect_time"
        ) as mock_set_custom_disconnect_time,
        patch(
            "universalassistant.components.motionblinds_ble.MotionDevice.set_permanent_connection"
        ) as set_permanent_connection,
    ):
        await options_update_listener(hass, mock_config_entry)
        mock_set_custom_disconnect_time.assert_called_once()
        set_permanent_connection.assert_called_once()


async def test_update_ble_device(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    service_info: BluetoothServiceInfoBleak,
) -> None:
    """Test async_update_ble_device."""

    await setup_integration(hass, mock_config_entry)

    with patch(
        "universalassistant.components.motionblinds_ble.MotionDevice.set_ble_device"
    ) as mock_set_ble_device:
        inject_bluetooth_service_info(hass, service_info)
        mock_set_ble_device.assert_called_once()
