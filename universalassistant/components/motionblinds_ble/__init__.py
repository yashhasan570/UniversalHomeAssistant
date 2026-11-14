"""Motionblinds Bluetooth integration."""

from functools import partial
import logging

from motionblindsble.const import MotionBlindType
from motionblindsble.crypt import MotionCrypt
from motionblindsble.device import MotionDevice

from universalassistant.components.bluetooth import (
    BluetoothCallbackMatcher,
    BluetoothChange,
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
    async_ble_device_from_address,
    async_register_callback,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ADDRESS, Platform
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.event import async_call_later
from universalassistant.helpers.typing import ConfigType

from .const import (
    CONF_BLIND_TYPE,
    CONF_MAC_CODE,
    DOMAIN,
    OPTION_DISCONNECT_TIME,
    OPTION_PERMANENT_CONNECTION,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.COVER,
    Platform.SELECT,
    Platform.SENSOR,
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

type MotionConfigEntry = ConfigEntry[MotionDevice]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up Motionblinds Bluetooth integration."""

    _LOGGER.debug("Setting up Motionblinds Bluetooth integration")

    # The correct time is needed for encryption
    _LOGGER.debug("Setting timezone for encryption: %s", hass.config.time_zone)
    MotionCrypt.set_timezone(hass.config.time_zone)

    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: MotionConfigEntry) -> None:
    """Set up Motionblinds Bluetooth device from a config entry."""

    _LOGGER.debug("(%s) Setting up device", entry.data[CONF_MAC_CODE])

    ble_device = async_ble_device_from_address(hass, entry.data[CONF_ADDRESS])
    device = MotionDevice(
        ble_device if ble_device is not None else entry.data[CONF_ADDRESS],
        blind_type=MotionBlindType[entry.data[CONF_BLIND_TYPE].upper()],
    )

    # Register __HA_KEEP__ functions to use in the library
    device.set_create_task_factory(
        partial(
            entry.async_create_background_task,
            hass=hass,
            name=device.ble_device.address,
        )
    )
    device.set_call_later_factory(partial(async_call_later, hass=hass))

    # Register a callback that updates the BLEDevice in the library
    @callback
    def async_update_ble_device(
        service_info: BluetoothServiceInfoBleak, change: BluetoothChange
    ) -> None:
        """Update the BLEDevice."""
        _LOGGER.debug("(%s) New BLE device found", service_info.address)
        device.set_ble_device(service_info.device, rssi=service_info.advertisement.rssi)

    entry.async_on_unload(
        async_register_callback(
            hass,
            async_update_ble_device,
            BluetoothCallbackMatcher(address=entry.data[CONF_ADDRESS]),
            BluetoothScanningMode.ACTIVE,
        )
    )

    # Register OptionsFlow update listener
    entry.async_on_unload(entry.add_update_listener(options_update_listener))

    entry.runtime_data = device

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Apply options
    entry.async_create_background_task(
        hass, apply_options(hass, entry), device.ble_device.address
    )

    _LOGGER.debug("(%s) Finished setting up device", entry.data[CONF_MAC_CODE])


async def options_update_listener(
    hass: __HAC_KEEP__, entry: MotionConfigEntry
) -> None:
    """Handle options update."""
    _LOGGER.debug(
        "(%s) Updated device options: %s", entry.data[CONF_MAC_CODE], entry.options
    )
    await apply_options(hass, entry)


async def apply_options(hass: __HAC_KEEP__, entry: MotionConfigEntry) -> None:
    """Apply the options from the OptionsFlow."""

    device = entry.runtime_data
    disconnect_time: float | None = entry.options.get(OPTION_DISCONNECT_TIME, None)
    permanent_connection: bool = entry.options.get(OPTION_PERMANENT_CONNECTION, False)

    device.set_custom_disconnect_time(disconnect_time)
    await device.set_permanent_connection(permanent_connection)


async def async_unload_entry(hass: __HAC_KEEP__, entry: MotionConfigEntry) -> None:
    """Unload Motionblinds Bluetooth device from a config entry."""

    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
