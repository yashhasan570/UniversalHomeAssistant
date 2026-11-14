"""The profiler integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DATA_PROFILER, DOMAIN
from .services import LOG_INTERVAL_SUB, async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up Profiler."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Profiler from a config entry."""


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    if LOG_INTERVAL_SUB in hass.data[DATA_PROFILER]:
        hass.data[DATA_PROFILER][LOG_INTERVAL_SUB]()
