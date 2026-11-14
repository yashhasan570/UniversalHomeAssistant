"""The BlueMaestro integration."""

import logging

from bluemaestro_ble import BlueMaestroBluetoothDeviceData

from universalassistant.components.bluetooth import BluetoothScanningMode
from universalassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type BlueMaestroConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: __HAC_KEEP__, entry: BlueMaestroConfigEntry) -> None:
    """Set up BlueMaestro BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    data = BlueMaestroBluetoothDeviceData()
    coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=data.update,
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(
        coordinator.async_start()
    )  # only start after all platforms have had a chance to subscribe


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: BlueMaestroConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
