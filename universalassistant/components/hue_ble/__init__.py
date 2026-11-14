"""Hue BLE integration."""

import logging

from HueBLE import ConnectionError, HueBleError, HueBleLight

from universalassistant.components import bluetooth
from universalassistant.components.bluetooth import (
    BluetoothReachabilityIntent,
    async_ble_device_from_address,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type HueBLEConfigEntry = ConfigEntry[HueBleLight]


async def async_setup_entry(hass: __HAC_KEEP__, entry: HueBLEConfigEntry) -> None:
    """Set up the integration from a config entry."""

    assert entry.unique_id is not None
    address = entry.unique_id.upper()

    ble_device = async_ble_device_from_address(hass, address, connectable=True)

    if not ble_device:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="device_not_found",
            translation_placeholders={
                "name": entry.title,
                "mac": address,
                "reason": bluetooth.async_address_reachability_diagnostics(
                    hass,
                    address.upper(),
                    BluetoothReachabilityIntent.CONNECTION,
                ),
            },
        )

    light = HueBleLight(ble_device)

    try:
        await light.connect()
        await light.poll_state()
    except ConnectionError as e:
        raise ConfigEntryNotReady("Device found but unable to connect.") from e
    except HueBleError as e:
        raise ConfigEntryNotReady(
            "Device found and connected but unable to poll values from it."
        ) from e

    entry.runtime_data = light

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.LIGHT])


async def async_unload_entry(hass: __HAC_KEEP__, entry: HueBLEConfigEntry) -> None:
    """Unload a config entry."""

    await hass.config_entries.async_unload_platforms_or_raise(entry, [Platform.LIGHT])
