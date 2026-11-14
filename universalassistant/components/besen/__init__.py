"""Besen Universal Universal Home Assistant integration."""

import logging

from besen.client import BesenClient
from besen.exceptions import CannotConnect, InvalidAuth
from bleak.backends.device import BLEDevice

from universalassistant.components import bluetooth
from universalassistant.components.bluetooth import BluetoothReachabilityIntent
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ADDRESS, CONF_NAME, CONF_PIN
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import BesenCoordinator
from .services import async_setup_services

type BesenConfigEntry = ConfigEntry[BesenCoordinator]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Besen integration."""

    async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: BesenConfigEntry,
) -> None:
    """Set up Besen from a config entry."""

    address = entry.data[CONF_ADDRESS]
    pin = entry.data[CONF_PIN]

    def _ble_device_provider() -> BLEDevice | None:
        return bluetooth.async_ble_device_from_address(
            hass,
            address,
            connectable=True,
        )

    if _ble_device_provider() is None:
        reason = bluetooth.async_address_reachability_diagnostics(
            hass,
            address,
            BluetoothReachabilityIntent.CONNECTION,
        )
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="no_connectable_path",
            translation_placeholders={"reason": reason},
        )

    client = BesenClient(
        address=address,
        pin=pin,
        ble_device_provider=_ble_device_provider,
        logger=_LOGGER,
        advertised_name=entry.data[CONF_NAME],
    )
    coordinator = BesenCoordinator(hass, entry, client)

    try:
        await coordinator.async_start()
    except InvalidAuth as err:
        raise ConfigEntryAuthFailed from err
    except CannotConnect as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
            translation_placeholders={"error": str(err)},
        ) from err

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant,
    entry: BesenConfigEntry,
) -> None:
    """Unload a Besen config entry."""

    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
