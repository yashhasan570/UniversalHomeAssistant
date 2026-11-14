"""The Energy integration."""

from universalassistant.components import frontend
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.typing import ConfigType

from . import websocket_api
from .const import DOMAIN
from .data import async_get_manager

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = [
    "DOMAIN",
    "async_get_manager",
    "is_configured",
]


async def is_configured(hass: __HAC_KEEP__) -> bool:
    """Return a boolean to indicate if energy is configured."""
    manager = await async_get_manager(hass)
    if manager.data is None:
        return False
    return bool(manager.data != manager.default_preferences())


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up Energy."""
    websocket_api.async_setup(hass)
    frontend.async_register_built_in_panel(hass, DOMAIN, DOMAIN, "mdi:lightning-bolt")

    hass.async_create_task(
        discovery.async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config),
        eager_start=True,
    )
    hass.data[DOMAIN] = {
        "cost_sensors": {},
    }

    return True
