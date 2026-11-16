"""The SensorPush Bluetooth integration."""

import logging

from sensorpush_ble import SensorPushBluetoothDeviceData

from universalassistant.components.bluetooth import BluetoothScanningMode
from universalassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type SensorPushConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: UniversalAssistant, entry: SensorPushConfigEntry) -> None:
    """Set up SensorPush BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=SensorPushBluetoothDeviceData().update,
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: UniversalAssistant, entry: SensorPushConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
