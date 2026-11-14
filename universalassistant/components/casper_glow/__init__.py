"""The Casper Glow integration."""

from pycasperglow import CasperGlow

from universalassistant.components import bluetooth
from universalassistant.components.bluetooth import BluetoothReachabilityIntent
from universalassistant.const import CONF_ADDRESS, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import CasperGlowConfigEntry, CasperGlowCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.SELECT,
    Platform.SENSOR,
]


async def async_setup_entry(hass: __HAC_KEEP__, entry: CasperGlowConfigEntry) -> None:
    """Set up Casper Glow from a config entry."""
    address: str = entry.data[CONF_ADDRESS]
    ble_device = bluetooth.async_ble_device_from_address(hass, address.upper(), True)
    if not ble_device:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="device_not_found",
            translation_placeholders={
                "address": address,
                "reason": bluetooth.async_address_reachability_diagnostics(
                    hass, address.upper(), BluetoothReachabilityIntent.CONNECTION
                ),
            },
        )

    glow = CasperGlow(ble_device)
    coordinator = CasperGlowCoordinator(hass, glow, entry.title)
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: __HAC_KEEP__, entry: CasperGlowConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
