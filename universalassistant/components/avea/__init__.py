"""The Avea integration."""

import avea

from universalassistant.components.bluetooth import (
    BluetoothReachabilityIntent,
    async_address_reachability_diagnostics,
    async_ble_device_from_address,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ADDRESS, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

type AveaConfigEntry = ConfigEntry[avea.Bulb]

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: UniversalAssistant, entry: AveaConfigEntry) -> None:
    """Set up Avea from a config entry."""
    address = entry.data[CONF_ADDRESS]
    ble_device = async_ble_device_from_address(hass, address, connectable=True)
    if not ble_device:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="device_not_found",
            translation_placeholders={
                "address": address,
                "reason": async_address_reachability_diagnostics(
                    hass,
                    address.upper(),
                    BluetoothReachabilityIntent.CONNECTION,
                ),
            },
        )

    entry.runtime_data = avea.Bulb(ble_device)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AveaConfigEntry) -> None:
    """Unload an Avea config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
