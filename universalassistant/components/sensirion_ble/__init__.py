"""The sensirion_ble integration."""

import logging

from sensirion_ble import SensirionBluetoothDeviceData

from universalassistant.components.bluetooth import BluetoothScanningMode
from universalassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type SensirionBluetoothConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: SensirionBluetoothConfigEntry
) -> None:
    """Set up Sensirion BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    data = SensirionBluetoothDeviceData()
    entry.runtime_data = coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.ACTIVE,
        update_method=data.update,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(
        coordinator.async_start()
    )  # only start after all platforms have had a chance to subscribe


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: SensirionBluetoothConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
