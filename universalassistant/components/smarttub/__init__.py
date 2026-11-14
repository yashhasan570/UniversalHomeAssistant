"""SmartTub integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .controller import SmartTubConfigEntry, SmartTubController
from .services import async_setup_services

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
]


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the SmartTub integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: SmartTubConfigEntry) -> None:
    """Set up a smarttub config entry."""

    controller = SmartTubController(hass)

    await controller.async_setup_entry(entry)

    entry.runtime_data = controller

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: SmartTubConfigEntry) -> None:
    """Remove a smarttub config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
