"""The Govee Bluetooth BLE integration."""

from functools import partial
import logging

from govee_ble import GoveeBluetoothDeviceData

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import (
    GoveeBLEBluetoothProcessorCoordinator,
    GoveeBLEConfigEntry,
    process_service_info,
)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.EVENT, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: UniversalAssistant, entry: GoveeBLEConfigEntry) -> None:
    """Set up Govee BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    data = GoveeBluetoothDeviceData()
    entry.runtime_data = coordinator = GoveeBLEBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        update_method=partial(process_service_info, hass, entry),
        device_data=data,
        entry=entry,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: UniversalAssistant, entry: GoveeBLEConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
