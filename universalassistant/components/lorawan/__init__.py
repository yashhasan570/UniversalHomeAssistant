"""The LoRaWAN integration."""

from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import Event, __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.service_info.lorawan import LoRaWANDiscoveryInfo
from universalassistant.helpers.typing import ConfigType
from universalassistant.loader import async_get_lorawan

from . import websocket_api
from .connection import DATA_REGISTRY, ConnectionRegistry, async_register_connection
from .const import DOMAIN
from .device_manager import DeviceManager, device_identifier
from .entity import LoRaWANEntity
from .validation import (
    NoConnectionsError,
    NoSupportedDevicesError,
    async_validate_devices,
)

__all__ = [
    "DeviceManager",
    "LoRaWANDiscoveryInfo",
    "LoRaWANEntity",
    "NoConnectionsError",
    "NoSupportedDevicesError",
    "async_register_connection",
    "async_validate_devices",
    "device_identifier",
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the LoRaWAN integration."""
    registry = hass.data[DATA_REGISTRY] = ConnectionRegistry(
        await async_get_lorawan(hass)
    )

    websocket_api.async_setup(hass)

    @callback
    def shutdown(event: Event) -> None:
        for registered in tuple(registry.connections.values()):
            registered.unsubscribe()
        registry.connection_change_listeners.clear()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, shutdown)
    return True
