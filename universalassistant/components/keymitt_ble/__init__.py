"""Integration to integrate Keymitt BLE devices with __HA_KEEP__."""

from microbot import MicroBotApiClient

from universalassistant.components import bluetooth
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_ADDRESS, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import MicroBotConfigEntry, MicroBotDataUpdateCoordinator
from .services import async_setup_services

PLATFORMS: list[str] = [Platform.SWITCH]


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Keymitt MicroBot Push integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: MicroBotConfigEntry) -> None:
    """Set up this integration using UI."""
    token: str = entry.data[CONF_ACCESS_TOKEN]
    bdaddr: str = entry.data[CONF_ADDRESS]
    ble_device = bluetooth.async_ble_device_from_address(hass, bdaddr)
    if not ble_device:
        raise ConfigEntryNotReady(f"Could not find MicroBot with address {bdaddr}")
    client = MicroBotApiClient(
        device=ble_device,
        token=token,
    )
    coordinator = MicroBotDataUpdateCoordinator(
        hass, client=client, ble_device=ble_device
    )

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: __HAC_KEEP__, entry: MicroBotConfigEntry) -> None:
    """Handle removal of an entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
