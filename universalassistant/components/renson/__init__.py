"""The Renson integration."""

from renson_endura_delta.renson import RensonVentilation

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import RensonConfigEntry, RensonCoordinator, RensonData
from .services import async_setup_services

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TIME,
]


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Renson integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: RensonConfigEntry) -> None:
    """Set up Renson from a config entry."""

    api = RensonVentilation(entry.data[CONF_HOST])
    coordinator = RensonCoordinator(hass, entry, api)

    if not await hass.async_add_executor_job(api.connect):
        raise ConfigEntryNotReady("Cannot connect to Renson device")

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = RensonData(
        api,
        coordinator,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: RensonConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
